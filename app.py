from flask import Flask, render_template, request, redirect, Response, abort, session, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

app = Flask(__name__)


#configararion
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#crazyusermodel
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="homepage")


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <html>
            <head>
             <link href="../static/css/bootstrap.min.css" rel="stylesheet" media="screen">
            </head>
        <body>
        <div class="container">
        <h1>Please login</h1>
        <br>
            <form action="" method="post">
                <p><input type=text name=username value={{
          request.form.username }}>
                <p><input type=password name=password value={{
          request.form.password }}>
                <p><input type=submit value=Login>
            </form>
            </div>
        </body>
        </html>
            ''')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


#A callback to reload
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == '__main__':
    app.run()
