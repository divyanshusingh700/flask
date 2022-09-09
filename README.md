Get started
===========

# How to deploy the docker container.

Installation
------------

### Install Docker for Windows 
Install docker from [this link](https://docs.docker.com/desktop/install/windows-install/)
### Install Docker for Linux 
Install docker from [this link](https://docs.docker.com/desktop/install/linux-install/)
### Install python [here](https://www.python.org/downloads/)
#### set PYTHON_HOME in environment variables

### For windows user Install Cygwin 
Install Cygwin from [this link](https://www.cygwin.com/install.html)


#### Create a project directory flask
Open cygwin terminal and cd to flask directory
#### Install virtual environment
```bash
$ pip install virtualenv
```
Activate virtual environment

```bash
$ virtualenv venv
$ source venv/scripts/activate
```

```bash
$ pip install flask
$ pip install pandas
$ pip install elasticsearch
$ pip freeze > requirements.txt
$ pip install -r requirements.txt
```
And now we are ready to go!

#### Test the flask application first on cygwin terminal by this command
```bash
$ flask run
```
#### Alternatively we first expose the application to development mode.
```bash
$ export FLASK_ENV=dev 
```
Usage
-----
If everything is fine then we would be able to see something like this. This is an example of running a service locally (`localhost`), using
port `5000`.
![flask run](https://user-images.githubusercontent.com/82446712/189286267-51158fb0-b506-45f2-893b-6c32fd7784e0.png)
## Next part is to create dockerfile
Usage
-----
The first line to add to a Dockerfile is a # syntax, this directive instructs the Docker builder what syntax to use when parsing the Dockerfile, and allows older Docker versions with BuildKit enabled to upgrade the parser before starting the build.
```bash
# syntax=docker/dockerfile:1
```
Next, we need to add a line in our Dockerfile that tells Docker what base image we would like to use for our application. I have mentioned here as a compiler only.
```bash
# syntax=docker/dockerfile:1
FROM python:3.9-slim as compiler
```
Next, we have to definr working directory of our application by doing this we do not have to type out full file paths but can use relative paths based on the working directory.
```bash
WORKDIR /flaskproduct
```
The COPY command takes two parameters.We will pass this copy command to copy the whole requirement API for building this application
```bash
COPY requirements.txt requirements.txt
```
Once we have our requirements.txt file inside the image, we can use the RUN command to execute the command pip3 install. This works exactly the same as if we were running pip3 install locally on our machine, but this time the modules are installed into the image.
```bash
RUN pip3 install -r requirements.txt
```
The EXPOSE command tells the image to run at the passed parameter port.
```bash
EXPOSE 5000
```
Next, Command is CMD which tells the image to run the elements in a list. This is similar to how you would run the Python application on your terminal using
```bash
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```
After doing this your dockerfile would look like this.
```bash
# syntax=docker/dockerfile:1

FROM python:3.9-slim as compiler
COPY . /flaskproduct
WORKDIR /flaskproduct
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```
Next we have to open the cygwin terminal in a virtual environment and run this command to build the image. In this command flaskapp is image name.
```bash
$ docker build --tag flaskapp .
```
Note: You might have to wait for 1 to 2 minutes.

If everything will be fine then it shows something like this
![cygwin](https://user-images.githubusercontent.com/82446712/189286000-e3417e77-7340-4b1c-bff1-b7bea8987e60.png)
#### Next  open the Docker Desktop and run the image
#### It would look like.
![docker](https://user-images.githubusercontent.com/82446712/189286861-6529313a-ce42-4e09-9144-61d801f8280f.png)

#### Next process is to test the endpoint /get_matched_products on Postman.
![postman](https://user-images.githubusercontent.com/82446712/189287353-188b0db3-f87d-4da2-adb2-79d02993dc3f.png)

# How to access APIs on localhost.
So, After completing all this step we can move forward to test our application on browser.
Note: Run this url on browser. Here localhost refers to 127.0.0.1
```bash
http://localhost:5000
```
#### It would look like this.
![Screenshot 2022-09-09 121330](https://user-images.githubusercontent.com/82446712/189288133-2b5a91f9-ad17-4146-a07e-932ec57690c8.png)

#### After uploading the sku list of csv file we would be redirected to the page with endpoint /get_matched_products.
#### It would look like this.

![download](https://user-images.githubusercontent.com/82446712/189288844-c484371d-e013-4fb6-97d1-3f1b76cf2002.png)

#### Clicking on the two link start the downloading of csv files

### SAMPLE JSON RESULT for machesfashion:
```json
[
  {
    "SKU": "6630340698814927",
    "Net-a-porter Product Name": "ZIMMERMANN Cassia scalloped floral-print linen mini dress",
    "Net-a-porter Product Brand": "zimmermann",
    "Net-a-porter Product Url": "https://www.net-a-porter.com/en-gb/shop/product/zimmermann/clothing/mini-dresses/cassia-scalloped-floral-print-linen-mini-dress/6630340698814927",
    "Net-a-porter Classification Level 1": "clothing",
    "Net-a-porter Regular Price": "775 GBP",
    "Net-a-porter Offer Price": "387.5 GBP",
    "Net-a-porter Stock": false,
    "Matchesfashion Product Name": "Cassia puff-sleeve floral-print voile mini dress ",
    "Matchesfashion Product Brand": "zimmermann",
    "Matchesfashion Product Url": "https://www.matchesfashion.com/products/Zimmermann-Cassia-puff-sleeve-floral-print-voile-mini-dress--1420469",
    "Matchesfashion Classification Level 1": "clothing",
    "Matchesfashion Regular Price": "775 GBP",
    "Matchesfashion Offer Price": "620 GBP",
    "Matchesfashion Stock": true
  },
  {
    "SKU": "34344356236882927",
    "Net-a-porter Product Name": "EXTREME CASHMERE N°53 Crew Hop neon cashmere-blend sweater",
    "Net-a-porter Product Brand": "extreme cashmere",
    "Net-a-porter Product Url": "https://www.net-a-porter.com/en-gb/shop/product/extreme-cashmere/clothing/round-neck/n-degrees-53-crew-hop-neon-cashmere-blend-sweater/34344356236882927",
    "Net-a-porter Classification Level 1": "clothing",
    "Net-a-porter Regular Price": "410 GBP",
    "Net-a-porter Offer Price": "410 GBP",
    "Net-a-porter Stock": true,
    "Matchesfashion Product Name": "No.53 Hop stretch-cashmere sweater",
    "Matchesfashion Product Brand": "extreme cashmere",
    "Matchesfashion Product Url": "https://www.matchesfashion.com/products/Extreme-Cashmere-No-53-Hop-stretch-cashmere-sweater-1471269",
    "Matchesfashion Classification Level 1": "clothing",
    "Matchesfashion Regular Price": "418 GBP",
    "Matchesfashion Offer Price": "418 GBP",
    "Matchesfashion Stock": true
  },
  {
    "SKU": "4394988609204371",
    "Net-a-porter Product Name": "CHRISTIAN LOUBOUTIN Velcrissimo spiked leather, canvas and rubber sandals",
    "Net-a-porter Product Brand": "christian louboutin",
    "Net-a-porter Product Url": "https://www.net-a-porter.com/en-gb/shop/product/christian-louboutin/shoes/flat/velcrissimo-spiked-leather-canvas-and-rubber-sandals/4394988609204371",
    "Net-a-porter Classification Level 1": "shoes",
    "Net-a-porter Regular Price": "575 GBP",
    "Net-a-porter Offer Price": "575 GBP",
    "Net-a-porter Stock": true,
    "Matchesfashion Product Name": "Velcrissimo neoprene sandals",
    "Matchesfashion Product Brand": "christian louboutin",
    "Matchesfashion Product Url": "https://www.matchesfashion.com/products/Christian-Louboutin-Velcrissimo-neoprene-sandals-1416478",
    "Matchesfashion Classification Level 1": "shoes",
    "Matchesfashion Regular Price": "575 GBP",
    "Matchesfashion Offer Price": "575 GBP",
    "Matchesfashion Stock": true
  }
]
```
### SAMPLE JSON RESULT for ssense and farfetch:
```json
[
  {
    "SKU": "6630340696440271",
    "Net-a-porter Product Name": "ALEXANDER WANG Sanford logo-print leather ankle boots",
    "Net-a-porter Product Brand": "alexander wang",
    "Net-a-porter Regular Price": "675 GBP",
    "Net-a-porter Offer Price": "337.5 GBP",
    "Ssense Product Name": "Black Stanford Boots",
    "Ssense Product Brand": "alexander wang",
    "Ssense Regular Price": "675 GBP",
    "Ssense Offer Price": "675 GBP",
    "Farfetch Product Name": "Sanford logo-detail boots",
    "Farfetch Product Brand": "alexander wang",
    "Farfetch Regular Price": "675 GBP",
    "Farfetch Offer Price": "405 GBP"
  },
  {
    "SKU": "4394988608924257",
    "Net-a-porter Product Name": "BOTTEGA VENETA Square Twist gold-plated and leather hoop earrings",
    "Net-a-porter Product Brand": "bottega veneta",
    "Net-a-porter Regular Price": "400 GBP",
    "Net-a-porter Offer Price": "400 GBP",
    "Ssense Product Name": "Gold & Yellow Leather Earrings",
    "Ssense Product Brand": "bottega veneta",
    "Ssense Regular Price": "400 GBP",
    "Ssense Offer Price": "400 GBP",
    "Farfetch Product Name": "twisted triangle hoop earrings",
    "Farfetch Product Brand": "bottega veneta",
    "Farfetch Regular Price": "465 GBP",
    "Farfetch Offer Price": "465 GBP"
  }
]
```
