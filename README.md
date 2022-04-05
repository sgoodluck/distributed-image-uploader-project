# Bowery Farming - Coding Assignment

<!-- markdownlint-disable MD033-->
<p align="center">
  <a href="https://boweryfarming.com/">
    <img src="https://www.refrigeratedfrozenfood.com/ext/resources/RFF/Bowery-Farming/Bowery_Wordmark_Seedling_Vertical_RGB_MidnightForest.jpg?1595449917" alt="Logo" height=72>
  </a>

  <h3 align="center">On-Premise Photo Uploader App</h3>

  <p align="center">
    A local API server that allows for uploading of images for eventual S3 backup. This solution was prepared by the following applicant for the position of Sr. Software Engineer at Bowery Farming
    <br>
    <a href="https://www.linkedin.com/in/sgoodluck">• Seth Martin •</a>
  </p>
</p>
<!-- markdownlint-enable MD033 -->

## Table of contents

- [Bowery Farming - Coding Assignment](#bowery-farming---coding-assignment)
  - [Table of contents](#table-of-contents)
  - [Quick start](#quick-start)
    - [Instructions for me](#instructions-for-me)
  - [Helpful Commands](#helpful-commands)
  - [Status](#status)
  - [Technologies used](#technologies-used)
  - [What's included](#whats-included)
  - [Requirements & Constraints](#requirements--constraints)
    - [Assumptions](#assumptions)
    - [Additional Considerations](#additional-considerations)
  - [Design & Process](#design--process)
    - [Process](#process)
    - [Design](#design)
  - [Discussions](#discussions)
  - [Thanks](#thanks)
  - [Copyright and license](#copyright-and-license)

## Quick start

The application consists of an NGINX load balancer handling several docker containers for the API. After downloading this, you can start the service with the following commands.

- Instruction 1
- Instruction 2
- Instruction 3

### Instructions for me

Prerequisites: python3, docker, docker-compose, nginx

1. Spin up a virtual environment: `python3 -m venv venv`
2. Activate it in the root directory: `. venv/bin/activate`
3. Install flask: `pip install Flask`
4. Install gunicorn: `pip install gunicorn`
5. To run just the flask server:
   1. Set environment variables: `export FLASK_APP=app.py` and `export FLASK_ENV=development`
   2. Run the server explicitly: `flask run`
6. To run the docker setup: `docker-compose up -d --build` 
7. To inspect docker instances: `docker ps`

## Helpful Commands

Docker volumes are tricky to access because they are actually VMs. That means you can't inspect them normally. So to inspect our shared volumes we are going to make a shorthand command to run a mini container that will let us inspect contents. Let's create an alias to make it easier.

`alias dm-disk='docker run --rm -it -v /:/docker alpine:edge $@'`

Now if we use `dm-disk ls -l /docker/var/lib/docker/volumes/` we will be able to see all of the volumes that we can access. To take a look at the photos stored on the machine, we would run this command for example:

`dm-disk ls -l /docker/var/lib/docker/volumes/bowery-onprem-uploader_photos/_data`

That will actually show us the list of photos in the persisted shared docker volume. Uploading to S3 won't be an issue as we would have another docker container that has direct volume access to invoke the lambda functions.

## Status

**19:02** Ok so we have successfully setup our docker-compose to spin up an nginx load balancer, 3 server instances, and can persist our photo data in a shared docker volume. We are pretty close. Next up, updating some instructions for use and demonstration and the endpoint to accept JSON instead of using a webform. Then we are pretty much there.

**17:34** Back to coding!

**16:30** Have another call - back soon

**16:15** Had some issues with my nginx config. But we now have our server scaling! So now it is time flesh out the actual upload endpoint. We will be creating a shared volume for our docker setup and storing files there.

**15:30** Time to review my notes and start programming! I know I'm going to be using docker volumes to hold data and the database, so I'll start with a simple scalable framework before implementing the actual upload because docker volumes can be tricky sometimes.

**14:05** I started working on this assignment a bit after noon. I have decided on the architecture and configuration for the app bearing in mind the assumptions provided. I also drafted up this markdown file for my own notes and to guide a reviewer. I feel comfortable with the design and will proceed to implement after a walk and some lunch.

## Technologies used

- python3 (w/ flask framework)
- nginx
- docker
- docker-compose
- postgres

## What's included

The app directory is as follows

```text
folder1/
└── folder2/
    ├── folder3/
    │   ├── file1
    │   └── file2
    └── folder4/
        ├── file3
        └── file4
```

## Requirements & Constraints

Bowery has over 1000 embedded devices each taking 2 photos every minute. To avoid network saturation, devices upload to a local API server which queues files locally to control S3 upload rate.

Using a programming language of your choice, build an API server that accepts image file uploads. **The api should have a single endpoint that receives a JSON payload and one key in that payload should be the image in binary format.** You may use any tools or libraries you see fit.

Additionally consider how the S3 upload and queing process should work to control outgoing upload rates. 

### Assumptions

- Local network upload speed is 200mbps
- Image file size averages 250kb
- Allocate 20% bandwidth resources for file uploads
- 1,000 devices upload 2 images per minute 

### Additional Considerations

- How do we handle variable network speed, file size, and bandwidth resources?
- How do we observe and monitor the system?
- How are we going to maintain system stability after completion?

## Design & Process

### Process

When given a somewhat nebulous task I usually do three things:

1. Read the requirements carefully and consider implications around provided constraints.
   - e.g. network speeds and file sizes hinted that a load balancer might be prudent
2. Spend 30-45 minutes researching to see what tools and libraries are available to aid in the process.
   - I considered trying this in Elixir but opted for Python due to familiarity and ease of communicability for others
3. Design and diagram the system prior to any coding as a means to determine "where to begin" and code efficiently

### Design

For this assignment, I opted to use **Python3** with the **flask** framework for expedient development. I chose **gunicorn** as the WSGI HTTP Server framework because it is simple and I wanted to try it. I also chose to containerize the app using **Docker** and coordinate the containers with **docker-compose**. I opted for **NGINX** to act as a load balancer for the servers. Lastly, I decided to implement a **postgres** database to track metadata around the images which could be used to coordinate S3 uploading and system clean up, mostly because I was having a good time.

Such a design could easily be shared across locations and scaled horizontally to handle additional IoT devices.

For uploading to S3, I would recommend the use of AWS Lambda functions to allow for concurrent and scalable uploads. Lambdas could be invoked from the on-premise servers, a separate sever, or run on an AWS cronjob to poll for image uploads. To reduce network congestion, polling invoking the lambdas is probably the better setup.

In short the system algorithm will work as follows:

1. Devices send images to a single NGINX endpoint
2. NGINX load balances file uploads across several servers
3. Each server accepts file and stores it in a shared docker volume and updates a local persistent SQL database with a file reference that includes location and status (uploaded, not uploaded, uploading, etc)
4. Query the SQL database to find photos not uploaded, upload to S3 using lambda functions, and update the status of each image reference on the DB upon success.
5. To control size of local filesystem a "cleaning" cronjob script can periodically check for successfully uploaded images and delete local versions

<!-- markdownlint-disable MD036-->
*Please note that for the purposes of this assigment, steps 4 and 5 have not been implemented and are explained here for design purposes only*
<!-- markdownlint-enable MD036-->

## Discussions

1. How do you think about uploading to S3 and the local queuing process?
2. How do we handle variable network speed, file size, and bandwidth resource allocation?
3. How should we observe and monitor the system?
4. How are we going to maintain system stability after completion?

## Thanks

This was a fun assignment! I particularly enjoy working on problems that have these real-world constraints and somewhat nebulous requirements. 

I'm absolutely open to feedback and understand that I may have missed some important considerations in this submission.

I look forward to feedback and hopefully diving into this design with the team in the near future.

## Copyright and license

Code released under the [MIT License](https://reponame/blob/master/LICENSEhttps://opensource.org/licenses/MIT).

Enjoy :smile:
