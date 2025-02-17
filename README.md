## Visit to the doctor

This project for the doctors or people who can create own profile and make an appointments with a doctor. 

Opportunities: </br>
&emsp;You need to register on this site. When you wiil register you need to choose who you are, 'Doctor' or not. If you choose will be 'Doctor' you can create a Doctor on your profile also you can edit profile, edit doctor, reset password, change password, write comments. If you don't check the box as a 'Doctor' when registering you will be like a 'Patient' and you can create comments, make an appointment with a doctor(date, time), edit profile, reset password, change password, remove appointments. </br>

How to install?
1. Clone this repository

        git clone https://github.com/scroynel/doctor.git
   
2. Create a virtual environment

        python -m venv env
    > env - name of environment

3. Install packages from file requirements.txt (Before that you need to go to the derictory where is a file 'requirements.txt')

        pip install -r requerements.txt

4. Run django project

        python manage.py runserver
   > `lsof -t -i:8000|xargs kill -9` if you default port is busy and you can't run django project
