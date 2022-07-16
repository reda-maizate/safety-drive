cd web_app
pip install --target ./package -r ../../requirements-web-app.txt
cd package
zip -r ../web_app.zip .
cd ..
zip -g web_app.zip templates
zip -g web_app.zip main.py
zip -g web_app.zip __init__.py
rm -rf package