# Machines Against Cards Against Humanity
#### CS 4701 Project
##### By Kaushik and Teddy

### Updating Django Database on Website

* SSH into the website
* cd to ~/public_html/cah/cardsAgainstHumanity
* `git pull`
* `python cah/manage.py syncdb --settings=cah.settings_web`
* `python cah/manage.py collectstatic --settings=cah.settings_web`
