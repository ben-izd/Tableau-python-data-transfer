Consider a JSON file like http://sample.com/file.json, as tableau 2021.1, there is no way to send that file directly to Tableau. Tableau has its own way to handle data from the web called Web Data Connector. In simple terms, you should run some JavaScript code before you handing the data to Tableau. With the help of Python `http` module, we could run a server and mimic a web page to send data directly from Python to Tableau.

# Sending Python data directly to Tableau
## Requirements:
- Python 3.5 and later (because `typing` module, you can remove type annotations to use for earlier versions)
- Because of `jquery` and `tableauwdc` javascript libraries, you and tableau should be able to connect to the internet
> Supported data types: `int`, `float`, `bool`, `str`, `datetime`, `date`, `None`\
> Your data should be a 2-dimensional array

1- Save `tableau_connector.py` beside your python file (we use `test.py` as sample)

2- in `test.py` import `tableau_connector`

3- call `setup` function which accepts two arguments: 
 - first arguments is your data
 - Second argument is port which is optional (default: 35000)
    
`test.py` code:
```python
import tableau_connector
import datetime

data = [[1, 2.5, True, "string", datetime.datetime(2020, 1, 1, 1, 1, 1), datetime.date(2020, 1, 1)], 
        [1, 2.5, True, None, datetime.datetime(2020, 1, 1, 1, 1, 1), datetime.date(2020, 1, 1)]]

tableau_connector.setup(data)
```
    
    
4- In Tableau, `Data` > `New Data Source` and choose `Web Data Connector`
type `127.0.0.1:35000` (or `localhost:35000`)

![](https://i.imgur.com/YUIWC4A.png)

5- Click `click here to load data`

6- After Tableau execute the code, click `Update Now` to see your data:

![](https://i.imgur.com/EZv1vLJ.png)

![](https://i.imgur.com/1M45AVq.png)


