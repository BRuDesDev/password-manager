# Password Manager v2 🤫🔐

An upgraded GUI-based password manager that securely stores user data locally. Originally built using Python and Tkinter, this revamped version now incorporates ttkbootstrap themes and styles, significantly enhancing its aesthetics.

### New features include:
	
     	    Preview Tab – Displays user input before saving, allowing confirmation in place of the old, primitive yes/no message box.     		
    	   Database Tab – Provides a visual representation of all saved entries from data.json, making it easier to manage stored passwords.
	Toggle Password - Click the 'Monkey' face to show password | Click the 'See No Evil Monkey' to toggle back to ******

This update brings a sleeker interface and a more intuitive user experience! <br>

### New App:
![Screen Shot 2025-02-14 at 2 56 29 PM](https://github.com/user-attachments/assets/08822b6a-6ef3-4c38-a7f1-bdb5533fa99f)
![Screen Shot 2025-02-14 at 2 56 55 PM](https://github.com/user-attachments/assets/80b47154-20eb-4b36-b72c-74d70097e597)


### Old App: 
![image](https://user-images.githubusercontent.com/103232802/162845696-a1cf63d8-128a-4d3d-a714-32e50d6834f9.png)
__________________________________________________________________________________________

### [If running in Linux]:
you may need to run in root mode (using 'sudo') to be able to create the password database on your local drive.<br>
If you get any errors (ImportError) you need to make sure all dependencies are installed.<br> 

Clone repository to your system:
![Screen Shot 2025-03-25 at 9 20 46 AM](https://github.com/user-attachments/assets/e910153b-4393-499d-ae34-f02a100a2f61)

<!> Consider using Python's virtual environment BEFORE installing dependencies from 'requirements.txt':
<!> Check out my tutorial on 'Python virtual Environments' <a linkhere

### Activate the virtual environment<br>
	source .venv/bin/activate <br>
<tab><tab><!> You can verify that you have activated your new env, and also that it is the correct env: 
	1. When you are inside a Virtual Environment
___________________________________________________________________________________

**INSTRUCTIONS** _for Installing and running the app_:<br><br>
	
**[in LINUX]** (debian, ubuntu, kali, etc.) terminal type these commands:<br>
<code>	
sudo mkdir ~/git      
</code><br>
<code>
sudo cd ~/git       
</code><br>
<code>
sudo git clone https://github.com/BRuDesDev/password-manager.git      
</code><br>
<code>
cd password-manager       
</code><br>
<code>
pip install -r requirements.txt
</code><br>
<code>
python3 main.py				
</code><br><br>
	
<t>**[in WINDOWS]**<br>
_Hopefully you have installed_ **Python IDLE** from python.org:<br>
<t>****In your files, browse to the **password-manager** folder cloned to your PC. Right-click on the **_main.py_** file and click _Open with_ --> **'Python 3.x'**<br>(see picture below 👇)<br><br>

![image](https://user-images.githubusercontent.com/103232802/162651068-e27cfe0a-de9e-4b76-9c30-e8b4c229c6dd.png)
