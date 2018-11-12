# HoMM3_browser_clone

### Some old game "clone" in browser. Now possible:
* 1) battle with different castles
* 2) some units can use original abilities
* 3) player can cast few tests spells with different skill lvl

### To start server follow this steps
You should have python version 3+
* 1) pip install -r requirements
* 2) python manage.py migrate
* 3) python manage.py collectstatic
* 3) python manage.py runserver  

Go to http://127.0.0.1:8000/

## TODO 
* 1) logging letters and numbers
* 2) API (which functionality?)
* * 1) auto tests (DB tests, login test, battle test with API)
* 3) auto tests (test all math, spells and units skill without API)
* 4) life tests (life test all units skills and spells)