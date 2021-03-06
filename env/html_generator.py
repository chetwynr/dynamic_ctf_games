import os

dirname = os.path.join( os.path.dirname( __file__ ))
root = os.path.join( os.path.dirname(dirname))
templates_path = os.path.join(root, 'templates')

template ="""

    <!doctype html>

    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
    
      <title>A Basic HTML5 Template</title>
      <meta name="description" content="A simple HTML5 Template for new projects.">
      <meta name="author" content="SitePoint">
    
      <meta property="og:title" content="A Basic HTML5 Template">
      <meta property="og:type" content="website">
      <meta property="og:url" content="https://www.sitepoint.com/a-basic-html5-template/">
      <meta property="og:description" content="A simple HTML5 Template for new projects.">
      <meta property="og:image" content="image.png">
    
      <link rel="icon" href="/favicon.ico">
      <link rel="icon" href="/favicon.svg" type="image/svg+xml">
      <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    
      <link rel="stylesheet" href="css/styles.css?v=1.0">
    
    </head>
    
    <body>
      <h1> Welcome to the random_episode </h1>
      
      <h3> Challenge Information for Demonstration: </h3>
      <p>
      
      The query:
      <br/>
      {{random_message}}
      
      <p>
      
      Example: Bool based solution: ' or 1=1 --
      <p/>
      
      
      
      <b>Example Data</b>: <br/>
      First Name: Kyle
      <br/>
      Surname: Smith
      <br/>
      Occupation: Occupational Therapist
      <br/>
      dob: 1975-01-02
      <br/>
      country: Finland
      
      <p>
      <b>Note: Demonstration only. No flag currently present in database.</b>
      <p>
       <b>/restart</b> will restart the flask application and generate a new challenge a new vulnerable query
       <br/>
       <b>Note:</b> Currently requires manual redirect to 127.0.0.1:5000
      
      <p>
      
      {{random_content}}
      
      <p>
      
    <form action ="/" method = "post">
        <p>
            {{form.p1.label}} {{form.p1(size=30)}} <br>
        </p>
            <p>
                {{form.p2.label}} {{form.p2(size=30)}} <br>
                
                
            </p>
            <p>
                
            </p>
            <p>
                {{form.submit()}}
            </p>
            
            <p>
            {{returned}}
            </p>
      
      <p>
      
      {{random_logic}}
      
    </body>
    </html>

    """

def saveTemplate():
    complete_path = os.path.join(templates_path, "random_index.html")
    contents = template

    f = open(complete_path, "w+")
    f.write(contents)
    f.close()


saveTemplate()
