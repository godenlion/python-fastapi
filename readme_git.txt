…or create a new repository on the command line
echo "# python-fastapi" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:godenlion/python-fastapi.git
git push -u origin main


…or push an existing repository from the command line
git remote add origin git@github.com:godenlion/python-fastapi.git
git branch -M main
git push -u origin main




+++++++++++++++++++++++++++++++++++++++++++++++++++++++
git init
git add --all
git commit -m "initial commit"

git config --global user.email you@example.com
git config --global user.name "Your Name"