mkdir venetia-build
cp -r utils venetia-build/utils
cp -r sites venetia-build/sites
cp -r helheim venetia-build/helheim
cp -r tls venetia-build/tls
cp -r tls_dist venetia-build/tls_dist
cp -r templates venetia-build/templates
cp -r static venetia-build/static
cp -r main.py venetia-build/main.py
cp -r favicon.ico venetia-build/favicon.ico

cd venetia-build

pyarmor pack -x " --advanced 2 --bootstrap 2 --enable-suffix --no-cross-protection --exclude helheim" -e " --add-data 'templates;templates' --add-data 'static;static' --add-data 'helheim;helheim' --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/user_agent/browsers.json';cloudscraper/user_agent --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/native.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/nodejs.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/js2py.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/chakracore.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/encapsulated.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/interpreters/jsunfuck.py';cloudscraper/interpreters --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/captcha/2captcha.py';cloudscraper/captcha --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/captcha/anticaptcha.py';cloudscraper/captcha --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/captcha/9kw.py';cloudscraper/captcha --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/captcha/deathbycaptcha.py';cloudscraper/captcha --add-data 'C:/Users/Charlie Bottomley/AppData/Local/Programs/Python/Python38/Lib/site-packages/cloudscraper/exceptions.py';cloudscraper --icon favicon.ico --onefile --hidden-import 'helheim' --hidden-import 'msgpack' --hidden-import 'lzstring' --hidden-import cloudscraper --hidden-import 'cryptography' --hidden-import 'polling'" --name venetiaCLI main.py
