python version:
Python 3.9.11

Steps to Run this Script

Step 1: Create python environment 
python -m venv myenv

Step 2: Activate environment
.\myenv\Scripts\activate

Step 3: Install requirements
pip install -r requirements.txt

Step 4: Make sure you have updated inupt_urls.list.csv file(optional)

Step 5: Run Program
python main.py
Enter 1 to crawl data form single page
Enter 2 to crawl data from multiple pages

Using Docker (if the above commands fail or do not work properly)
docker-compose up --build
"This is will run single page crawl"

I acknowledge that extracting address data may currently be less accurate. However, it can be significantly improved to achieve over 90% accuracy by integrating AI tools or advanced Python libraries