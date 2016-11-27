## Dependencies ###


  ```bash
  pip install -r requirements.txt
  ```
  
# Usage

Make sure that the dependencies listed below are met, and then run the commands
to start the server,

```bash
python manage.py migrate
python manage.py runserver
```


## Worker instructions

Load the URL of the tool (by default
[http://localhost:8000](http://localhost:8000)) in your browser. Click on
**List of HITs**, and then start completing the HITs under the **Unfinished
HITs**

## Requester instructions

```bash
python manage.py publish_hits <template_file_path> <csv_file_path>
```

```bash
python manage.py dump_results <template_file_path> <results_csv_file_path>
```
