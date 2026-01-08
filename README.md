# raven_ai
test project with python, ravendb and AI agents


# envirnoment instructions

```bash
conda env create -f environment.yml
conda activate raven_ai
```

# start RavenDB
```bash
cd RavenDB
./run.sh
```

# start application

```bash
python ./main.py
```

# create the docs

```bash
cd  ./docs
make html
```
The html/ folder is created . Open index.html on a web browser.

# ollama instructions
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl status ollama
sudo systemctl start ollama
sudo systemctl stop ollama
sudo nano /etc/systemd/system/ollama.service
Environment="OLLAMA_HOST=0.0.0.0"
```

# Documentation
[Isaac Raven_AI readthedocs](https://raven-ai.readthedocs.io/)
