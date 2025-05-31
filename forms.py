from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField,
    IntegerField, BooleanField, SubmitField, FloatField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length,
    Optional, NumberRange, URL, ValidationError
)


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('I am a', choices=[
        ('client', 'Client - I want to hire freelancers'),
        ('freelancer', 'Freelancer - I want to work on projects')
    ])
    submit = SubmitField('Sign Up')


class ClientProfileForm(FlaskForm):
    """Client profile edit form"""
    company_name = StringField('Company Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    industry = StringField('Industry', validators=[
        DataRequired(),
        Length(max=100)
    ])
    website = StringField('Website', validators=[
        Optional(),
        URL()
    ])
    description = TextAreaField('Company Description', validators=[
        Optional(),
        Length(max=1000)
    ])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=100)
    ])
    profile_pic = FileField('Profile Picture', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')

# Modify the FreelancerProfileForm in forms.py
class FreelancerProfileForm(FlaskForm):
    """Freelancer profile edit form"""
    domain = SelectField('Domain/Specialization', choices=[
        ('Web Development', 'Web Development'),
        ('Mobile App Development', 'Mobile App Development'),
        ('Data Science', 'Data Science'),
        ('Content Writing', 'Content Writing'),
        ('Graphic Design', 'Graphic Design'),
        ('Digital Marketing', 'Digital Marketing'),
        ('Cybersecurity', 'Cybersecurity')
    ])
    # Change the skills field from StringField to SelectMultipleField
    skills = SelectMultipleField('Skills',
                               choices=[
                                   ('HTML', 'HTML'),
                                   ('CSS', 'CSS'),
                                   ('JavaScript', 'JavaScript'),
                                   ('React', 'React'),
                                   ('Node.js', 'Node.js'),
                                   ('Python', 'Python'),
                                   ('Django', 'Django'),
                                   ('Flask', 'Flask'),
                                   ('PHP', 'PHP'),
                                   ('Laravel', 'Laravel'),
                                   ('MySQL', 'MySQL'),
                                   ('PostgreSQL', 'PostgreSQL'),
                                   ('MongoDB', 'MongoDB'),
                                   ('AWS', 'AWS'),
                                   ('Azure', 'Azure'),
                                   ('Docker', 'Docker'),
                                   ('Kubernetes', 'Kubernetes'),
                                   ('Git', 'Git'),
                                   ('Flutter', 'Flutter'),
                                   ('React Native', 'React Native'),
                                   ('Android', 'Android'),
                                   ('iOS', 'iOS'),
                                   ('SEO Writing', 'SEO Writing'),
                                   ('Blog Posts', 'Blog Posts'),
                                   ('Copywriting', 'Copywriting'),
                                   ('Editing', 'Editing'),
                                   ('Graphic Design', 'Graphic Design'),
                                   ('Logo Design', 'Logo Design'),
                                   ('UI Design', 'UI Design'),
                                   ('UX Design', 'UX Design'),
                                   ('Data Science', 'Data Science'),
                                   ('Machine Learning', 'Machine Learning'),
                                   ('Data Analysis', 'Data Analysis'),
                                   ('Social Media Marketing', 'Social Media Marketing')
                               ],
                               validators=[DataRequired()])
    bio = TextAreaField('Professional Bio', validators=[
        DataRequired(),
        Length(max=1000)
    ])
    experience = StringField('Experience', validators=[
        DataRequired(),
        Length(max=50)
    ])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=100)
    ])
    hourly_rate = IntegerField('Hourly Rate (INR)', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    linkedin = StringField('LinkedIn Profile', validators=[
        Optional(),
        URL()
    ])
    portfolio_url = StringField('Portfolio Website', validators=[
        Optional(),
        URL()
    ])
    profile_pic = FileField('Profile Picture', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')


# Add this to your forms.py file

class MessageForm(FlaskForm):
    """Form for sending messages"""
    content = StringField('Message', validators=[DataRequired()],
                         render_kw={"placeholder": "Type your message here..."})
    submit = SubmitField('Send')

class PostForm(FlaskForm):
    """Project posting form"""
    title = StringField('Project Title', validators=[
        DataRequired(),
        Length(min=5, max=200)
    ])
    description = TextAreaField('Project Description', validators=[
        DataRequired(),
        Length(min=20, max=2000)
    ])
    skills = SelectMultipleField('Required Skills',
                                 choices=[
                                     ('HTML', 'HTML'),
                                     ('CSS', 'CSS'),
                                     ('JavaScript', 'JavaScript'),
                                     ('React', 'React'),
                                     ('Node.js', 'Node.js'),
                                     ('Python', 'Python'),
                                     ('Django', 'Django'),
                                     ('Flask', 'Flask'),
                                     ('PHP', 'PHP'),
                                     ('Laravel', 'Laravel'),
                                     ('MySQL', 'MySQL'),
                                     ('PostgreSQL', 'PostgreSQL'),
                                     ('MongoDB', 'MongoDB'),
                                     ('AWS', 'AWS'),
                                     ('Azure', 'Azure'),
                                     ('Docker', 'Docker'),
                                     ('Kubernetes', 'Kubernetes'),
                                     ('Git', 'Git'),
                                     ('Flutter', 'Flutter'),
                                     ('React Native', 'React Native'),
                                     ('Android', 'Android'),
                                     ('iOS', 'iOS'),
                                     ('SEO Writing', 'SEO Writing'),
                                     ('Blog Posts', 'Blog Posts'),
                                     ('Copywriting', 'Copywriting'),
                                     ('Editing', 'Editing'),
                                     ('Graphic Design', 'Graphic Design'),
                                     ('Logo Design', 'Logo Design'),
                                     ('UI Design', 'UI Design'),
                                     ('UX Design', 'UX Design'),
                                     ('Data Science', 'Data Science'),
                                     ('Machine Learning', 'Machine Learning'),
                                     ('Data Analysis', 'Data Analysis'),
                                     ('Social Media Marketing', 'Social Media Marketing')
                                 ],
                                 validators=[DataRequired()])

    keywords = SelectMultipleField('Keywords',
                                   choices=[
                                       ('responsive', 'Responsive'),
                                       ('frontend', 'Frontend'),
                                       ('backend', 'Backend'),
                                       ('web', 'Web'),
                                       ('design', 'Design'),
                                       ('interactive', 'Interactive'),
                                       ('dynamic', 'Dynamic'),
                                       ('single page', 'Single Page'),
                                       ('web app', 'Web App'),
                                       ('api', 'API'),
                                       ('server', 'Server'),
                                       ('data science', 'Data Science'),
                                       ('automation', 'Automation'),
                                       ('scripting', 'Scripting'),
                                       ('framework', 'Framework'),
                                       ('database', 'Database'),
                                       ('storage', 'Storage'),
                                       ('nosql', 'NoSQL'),
                                       ('cloud', 'Cloud'),
                                       ('deployment', 'Deployment'),
                                       ('infrastructure', 'Infrastructure'),
                                       ('container', 'Container'),
                                       ('devops', 'DevOps'),
                                       ('version control', 'Version Control'),
                                       ('collaboration', 'Collaboration'),
                                       ('mobile', 'Mobile'),
                                       ('cross-platform', 'Cross-Platform'),
                                       ('app', 'App'),
                                       ('content', 'Content'),
                                       ('optimization', 'Optimization'),
                                       ('marketing', 'Marketing'),
                                       ('writing', 'Writing'),
                                       ('sales', 'Sales'),
                                       ('proofreading', 'Proofreading'),
                                       ('quality', 'Quality'),
                                       ('visual', 'Visual'),
                                       ('creative', 'Creative'),
                                       ('branding', 'Branding'),
                                       ('identity', 'Identity'),
                                       ('interface', 'Interface'),
                                       ('user experience', 'User Experience'),
                                       ('usability', 'Usability'),
                                       ('analytics', 'Analytics'),
                                       ('algorithms', 'Algorithms'),
                                       ('statistics', 'Statistics'),
                                       ('insights', 'Insights'),
                                       ('visualization', 'Visualization'),
                                       ('promotion', 'Promotion')
                                   ],
                                   validators=[Optional()])
    budget = IntegerField('Budget (INR)', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    duration = StringField('Estimated Duration', validators=[
        DataRequired(),
        Length(max=100)
    ])
    submit = SubmitField('Post Project')


class BidForm(FlaskForm):
    """Bid creation form"""
    amount = IntegerField('Bid Amount (INR)', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    proposal = TextAreaField('Proposal / Cover Letter', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Proposal should be between 50 and 1000 characters')
    ])
    delivery_time = StringField('Delivery Time', validators=[
        DataRequired(),
        Length(max=100)
    ])
    submit = SubmitField('Submit Bid')


class ReviewForm(FlaskForm):
    """Freelancer review form"""
    rating = FloatField('Rating (1-5)', validators=[
        DataRequired(),
        NumberRange(min=1, max=5)
    ])
    review_text = TextAreaField('Review', validators=[
        Optional(),
        Length(max=500)
    ])
    submit = SubmitField('Submit Review')


class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Search', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    search_type = SelectField('Type', choices=[
        ('freelancers', 'Freelancers'),
        ('projects', 'Projects')
    ])
    submit = SubmitField('Search')


class ContactForm(FlaskForm):
    """Contact/message form"""
    subject = StringField('Subject', validators=[
        DataRequired(),
        Length(max=100)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
    submit = SubmitField('Send Message')