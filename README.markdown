## Installation ###

  ```bash
  pip install -r requirements.txt
  ```
  
# Usage

First run the commands to start the server,

```bash
python manage.py migrate
python manage.py runserver
```

## Publish HITS

```bash
python manage.py publish_hits <template_file_path> <csv_file_path>
```

## Start Annotating

Load the URL of the tool (by default
[http://localhost:8000](http://localhost:8000)) in your browser. Click on
**List of HITs**, and then start completing the HITs under the **Unfinished
HITs**

## Compile Annotations

```bash
python manage.py dump_results <template_file_path> <results_csv_file_path>
```
