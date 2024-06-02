
# Music Streaming Application V-2

A multi-user application which allows users to listen to songs, , read lyrics,create playlists, upload songs and albums,etc. 




## Requirements 

- Project Zip File
- Windows OS with WSL
- Python 3.10
- Browser:Chrome or Firefox
- Terminal: WSL
- Npm or Yarn
- redis-server installation
```bash
 # install redis
 $ sudo apt install redis-server
```
- MailHog Installation
```bash
# install go
$ sudo apt install golang-go

# install mailhog
$ go install github.com/mailhog/MailHog@latest
```




## Run Locally



Clone the project OR download the zip file
```bash
  git clone https://link-to-project
```

The project requires 6 terminals

- Terminal-1 (Backend)

  - Go to the project backend

    ```bash
    $ cd Project/backend
    ```

  - Create and activate virtual environment
       ```bash
        $ python3 -m venv .env
        $ source .env/bin/activate

   - Install dependencies
        ```bash
        $ pip install -r requirements.txt
        ``` 

    - Start the backend server

            $ python3 app.py
- Terminal-2 (Frontend)

     - Go to the project frontend

            $ cd Project/frontend

     - Install dependencies

            $ npm install
     -  Start the frontend server

            $ npm run dev
- Terminal-3 (Redis)

     - Start the redis-server

            # stop if redis is already running
            $ sudo systemctl stop redis

            # start redis-server
            $ redis-server
- Terminal-4 (MailHog)

    - Start MailHog server

            $ ~/go/bin/MailHog
- Terminal-5 (Celery-worker)

     - Go to the project backend

            $ cd Project/backend
  - Start celery-worker

        $ celery -A app:celery_app worker -l INFO
- Terminal-6 (Celery-Beat)

    - Go to the project backend

            $ cd Project/backend
    - Start celery-beat

            $ celery -A app:celery_app beat -l INFO
Open your browser and navigate to http://localhost:5173
