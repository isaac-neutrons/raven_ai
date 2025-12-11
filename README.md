# raven_ai
test project with Node.js, ravendb and AI agents


# installation instructions

node-environment creation/activation

```bash
pip install nodeenv
nodeenv raven
source raven/bin/activate
npm install --save ravendb
npm install --save express

deactivate_node
```

# start RavenDB
```bash
cd RavenDB
./run.sh
```

# start application

```bash
node index.js
```

# ollama instructions
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl status ollama
sudo systemctl start ollama
sudo systemctl stop ollama
sudo nano /etc/systemd/system/ollama.service
Environment="OLLAMA_HOST=0.0.0.0"
```


https://github.com/ravendb/ravendb-python-client/tree/v7.1
