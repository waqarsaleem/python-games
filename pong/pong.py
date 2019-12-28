import operator
import turtle

# Window.
wn = turtle.Screen()
wn.title("Pong by @waqarsaleem")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Paddles and Ball.


def get_square():
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.penup()
    return paddle


paddle_a: turtle.Turtle = get_square()
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.goto(-350, 0)
paddle_b: turtle.Turtle = get_square()
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.goto(350, 0)
ball: turtle.Turtle = get_square()
ball.goto(0, 0)

# Movement


def move_up(paddle: turtle.Turtle):
    y: int = paddle.ycor()
    y += 20
    paddle.sety(y)


def move_down(paddle: turtle.Turtle):
    y: int = paddle.ycor()
    y -= 20
    paddle.sety(y)


wn.listen()
wn.onkeypress(lambda: move_up(paddle_a), "w")
wn.onkeypress(lambda: move_down(paddle_a), "s")
wn.onkeypress(lambda: move_up(paddle_b), "Up")
wn.onkeypress(lambda: move_down(paddle_b), "Down")

ball.dx: int = 2
ball.dy: int = 2

# Pause, close game.
pause = False


def toggle_pause():
    global pause
    pause = not pause
    print(f'pause: pause')


wn.onkeypress(toggle_pause, "p")
wn.onkeypress(wn.bye, "q")


# Borders for bouncing off - ball is a square of 20 with origin at top left
ball_height = ball_width = 20
window_right = wn.window_width() // 2
window_left = -window_right
window_top = (wn.window_height() - ball_height) // 2
window_bottom = -wn.window_height() // 2 + ball_height


# Main game loop.
while True:
    if pause:
        continue
    wn.update()
    # Move the ball.
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border check - bounce ball off window top/bottom.
    if ball.ycor() > window_top:
        ball.sety(window_top)
        ball.dy *= -1
    if ball.ycor() < window_bottom:
        ball.sety(window_bottom)
        ball.dy *= -1
    # Border check - continue ball from center after passing window left/right.
    if ball.xcor() < window_left:
        ball.goto(0, 0)
        ball.dx *= -1
    if ball.xcor() > window_right:
        ball.goto(0, 0)
        ball.dx *= -1
    # Bounce ball off paddles.
    if -20 < ball.xcor() - paddle_b.xcor() < -10 and \
       -60 < ball.ycor() - paddle_b.ycor() < 60:
       # ball.ycor()-10 < paddle_b.ycor()+50 and \
       # ball.ycor()+10 > paddle_b.ycor()-50:
        ball.dx *= -1
