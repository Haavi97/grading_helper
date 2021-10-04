import os


from get_codes import get_files_with_code
import random_table

html_intro = """<!DOCTYPE html>
<html>

<header>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
    font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg .tg-glna{background-color:#fffe65;text-align:left;vertical-align:top}
    .tg .tg-kd4e{background-color:#34ff34;text-align:left;vertical-align:top}
    </style>
</header>
<body>

    <h1>Grading other students</h1>
    <p>Your task is to grade 2 different packages. Your UniID (truncated to the 6 digits) is listed below along with the ID of the 2 packages you must grade. </p>
    <p>The grading sheet link is available on Moodle under the lab2 section. (Also here:
    <a href="https://docs.google.com/forms/d/e/1FAIpQLScPe6kN46C1WS9ynJlVZMlNFK2B-CnsJP4rDzEqGbm9vcbSsw/viewform?usp=sf_link">Link to the grading sheet. </a>)
    You can find all the packages below.</p>
    <p>Download the 2 packages you have to grade and follow the instructions on the grading sheet. The deadline to grade is Friday evening 23:59.</p>
    <p>If the grading is not done correctly, or not at all by Friday 23:59, you will get a 30% penalty on your own grade.</p>
    <p>The teaching assistants will grade some of you picked randomly and assess at the same time the grading quality of the 2 or 3 graders.</p>
    <table class="tg">
    <thead>
    <tr>
        <th class="tg-kd4e">Grader</th>
        <th class="tg-glna" colspan="2">Packages to grade</th>
    </tr>
    </thead>
"""
table_closing = """
    </tbody>
    </table>
    <br>

    <h1>List of files:</h1>

"""
html_closing = """
</body>

</html>"""

def to_html(html_fn='index.html'):
    with open(html_fn, 'w') as f:
        f.write(html_intro)
        students_dict = random_table.randomize_student_codes()
        for code in students_dict:
            f.write("""<tr>
        <td class="tg-kd4e">{}</td>
        <td class="tg-glna">{}</td>
        <td class="tg-glna">{}</td>
    </tr>""".format(code, students_dict[code][0], students_dict[code][1]))
    
        for file in get_files_with_code():
            f.write("<a href=" + file + ">" + file + "</a> </br>")
        f.write(table_closing)
        f.write(html_closing)


if __name__ == '__main__':
    to_html()
