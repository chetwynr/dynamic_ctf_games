#### Dynamic HTML Generator WIP

class body():
    def __init__(self):
        ### Minimums
        self.start = "<body>\n"
        self.close = "</body>\n"
        self.content = "Hello World"

        self.form_inputs = 0
        self.formStart = "<form>\n"
        self.formEnd = "</form>\n"


    def forms(self,action,form_inputs):
        count = 0
        form_list = []

        while count < form_inputs:
            input = str(count)
            string = "{{form.count["+input+"]}}\n"
            action = action
            form_list.append(string)
            count +=1

        return form_list,action
    def buildBody(self):
        returned_list =

        template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Index</title>
        </head>
        {}
        {}
        {}
        {}
        {}
        {}
        {}
        
        
        """.format(self.start,self.close,self.content,self.formStart,,self.formEnd)






p1 = body()
p1.forms("index.php",3)

template = """
<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Index</title>
    </head>
    <body>
    <p>Hello World<p>
    </body>
    </html>    
        """

'''def output(name):

    file = open(name,"w")
    file.write(template)

output("test.html")'''
