from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/euler1/<int:index>')
def euler1(index):

	total = 0
	
	while(index > 0):
	
		index -= 1

		if(index % 5 == 0 or index % 3 == 0):
			total += index

	return (str(total))

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'Paul %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
