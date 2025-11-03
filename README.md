# raven_ai
test project with Node.js, raven and AI agents

# installation instructions
# nodeenvironment creation/activation
pip install nodeenv
nodeenv raven
source raven/bin/activate
npm install --save ravendb
npm install --save express

deactivate_node

# start
node index.js


# ollama instructions
curl -fsSL https://ollama.com/install.sh | sh
systemctl status ollama
sudo systemctl stop ollama
sudo nano /etc/systemd/system/ollama.service
Environment="OLLAMA_HOST=0.0.0.0"
