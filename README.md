# HackDuke22
### Inequality track: Blinder Resume

## Inspiration
Initial resume screening is an important step where recruiters' bias plays a great role in discrimination. Applicants are highly discriminated against based on their race and gender in this step. Applicants with 'white names' and 'male names' are multiple times more likely to receive an invitation for an interview that their counterparts with 'non-white names' and 'female names'. To combat this we are creating a program to anonymize and generalize applicants' resume elements to create a more blind and equal-opportunity resume screening process.

## What it does
Based on our research the main identifying elements of a resume for race and gender are name, contact information, and extracurriculars. As such, our program reads a resume and hides name, and contact information from the recruiter. In addition, still in development, it generalizes extracurricular activities in the resume so that recruiters have good information about the applicant's interests and efforts without consciously or unconsciously discriminating against them based on the types and details of the activities.

## How we built it
We used python libraries to read and parse the resumes of applicants. Following that we used Open AI's GPT-3 to run NLP and extract relevant information regardless of the formatting of the resume. Following that, still in development, we further utilized GPT-3 to generalize and categorize extracurriculars and other points based on which potential discrimination can occur. We used Django to combine these elements together in a web app. We developed a front end both for the recruiter and the applicant. For the applicant, after submitting information and resume, the information is removed from the resume, and contact information is saved in a separate database where it can be fetched by the program. In case the recruiter wants to select the applicant for an interview, then a simple click can send an email to the applicant.

## Challenges we ran into
The major challenges we ran into is standardizing the format of resumes. Resumes come in many forms and parsing them through GPT-3 the resulting json willl have many branches with different height. It was challenging finding formats and representations of these brances in a django template.

## Accomplishments that we're proud of
Even though we have yet to complete some features, we were able to come up with a worthy idea and solution that solves a problem we are currently facing ourselves. 

## What we learned
We learned project planning and management. In addition, we were able to learn the features of an efficient team, specifically goal clarity and role distinction. 

## What's next for Blinder Resume
We plan to complete, improve, and test our program. Following that, we plan to find partners with whom we can implement the program and study the changes that come from using this program. Based on these results we will continue to improve on the program and further develop it into a stage where it can fight inequality in resume screening.
# HackDuke22
