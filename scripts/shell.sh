cd Aula-GitHub-Actions
ls
pwd
sudo apt-get install mailutils -y
echo "Pipeline executado com sucesso!" | mail -s "Pipeline status" "$DESTINATION_EMAIL"
