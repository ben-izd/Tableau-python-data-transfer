from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
from typing import List,Dict,Union,TypeVar
from platform import python_version
import json
import re
from functools import reduce


Date_Type = TypeVar('Date_Type', datetime.datetime,datetime.date)
Element_Type = TypeVar('Element_Type', float,int,str,datetime.date,datetime.datetime,bool)
Data_List_Type = List[List[Union[Element_Type]]]


def date_to_string(data:Date_Type) -> str:    
    return f'new Date({",".join(map(str,list(data.timetuple())[:-3]))})'

def generate_html(data:Data_List_Type,headers:List[str]=None) -> str:

    temp_data:List[List] = []
    if headers is None:
        headers = []
    
    # if headers are not enough, create headers base on the first row
    if len(data[0]) > len(headers):
        headers = [f'C{i}' for i in range(1,len(data[0])+1)]
    
    types:Dict[str, str] = {
        'float' : "tableau.dataTypeEnum.float", 
        'int': "tableau.dataTypeEnum.int",
        'str' : "tableau.dataTypeEnum.string",
        'date': "tableau.dataTypeEnum.date",
        'datetime': "tableau.dataTypeEnum.datetime",
        'bool': "tableau.dataTypeEnum.bool"
    }

    cols:str = json.dumps([{'id':headers[i],'dataType':types.get(type(v).__name__,'null')} for i,v in enumerate(data[0])])

    # remove " wrapped around specific words
    cols = reduce(lambda a,b:a.replace('"'+b+'"',b),list(types.values())+['id','dataType','null'],cols)
    
    for rowi in range(len(data)):
        temp_data.append({headers[i]:v if not isinstance(v,datetime.date) else date_to_string(v) for i,v in enumerate(data[rowi])})

    
    html_template='''<!DOCTYPE html>
<html lang="en">
<head>
<title></title>
<meta http-equiv="Cache-Control" content="no-store" />
<meta charset="UTF-8">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
<script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
<script>
(function() {
    
    var myConnector = tableau.makeConnector();

    myConnector.getSchema = function(schemaCallback) {
        var cols = '''+cols+''';

        var tableSchema = {
            id: "python",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    myConnector.getData = function(table, doneCallback) {
        table.appendRows('''+json.dumps(temp_data)+''');
        doneCallback();
    };

    tableau.registerConnector(myConnector);

    $(document).ready(function () {
        $("#submitButton").click(function () {
            tableau.connectionName = "Python";
            tableau.submit();
        });
    });

})();

</script>
</head>
<body>
<button id="submitButton">Click here to load</button>
</body>
</html>'''

    return re.sub(r'\"new Date\(((?:\d+\,){5}\d+)\)\"',r'new Date(\1)',html_template)

def setup(data:Data_List_Type,port:int=34000):
    '''
    Input:
    - data :List[List] : the data which will be used in tableau
    supported types: int, float, string, bool, date, datetime

    - port :int : default is on 34000
    '''

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Server", f"Python/{python_version()}")
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Date", f'{datetime.datetime.now(datetime.timezone.utc)}')
            self.send_header("Vary","Accept-Encoding")
            self.end_headers()
            self.wfile.write(bytes(generate_html(data=data), "utf-8"))
            

    webServer = HTTPServer(("localhost", port), MyServer)
    print(f"Server started http://localhost:{port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.") 