import os
import turtle

# Window.
wn = turtle.Screen()
wn.title("Pong by @waqarsaleem")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score and display.
score_a = score_b = 0
bounces = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Player A: 0 Player B: 0", align="center",
          font=("Courier", 24, "normal"))


# Help lines.
colors = ['white', 'gray', 'white']
ys = [300, 0, -300]
for i in range(3):
    line = turtle.Turtle()
    line.hideturtle()
    line.speed(0)
    line.color(colors[i])
    line.penup()
    line.goto(-400, ys[i])
    line.pendown()
    line.goto(400, ys[i])
line.color('gray')
line.penup()
line.goto(0, 300)
line.pendown()
line.goto(0, -300)

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


def reset_speeds():
    ball.dx: int = 2
    ball.dy: int = 2
    paddle_a.dy = 20
    paddle_b.dy = 20


def accelerate_ball():
    if ball.dx > 0:
        ball.dx += 1
    elif ball.dx < 0:
        ball.dx -= 1
    if ball.dy > 0:
        ball.dy += 1
    elif ball.dy < 0:
        ball.dy -= 1
    print('Accelerated ball.')


def accelerate_paddles():
    paddle_a.dy += 1
    paddle_b.dy += 1
    print('Accelerated paddles.')


def move_up(paddle: turtle.Turtle):
    global started
    if not started:
        return
    y: int = paddle.ycor()
    y = min(y + paddle.dy, 250)
    paddle.sety(y)


def move_down(paddle: turtle.Turtle):
    global started
    if not started:
        return
    y: int = paddle.ycor()
    y = max(y - paddle.dy, -250)
    paddle.sety(y)


wn.listen()
wn.onkeypress(lambda: move_up(paddle_a), "a")
wn.onkeypress(lambda: move_down(paddle_a), "z")
wn.onkeypress(lambda: move_up(paddle_b), "Up")
wn.onkeypress(lambda: move_down(paddle_b), "Down")
reset_speeds()

# Game states.
started = paused = False
start_message = pause_message = turtle.Turtle()
start_message.hideturtle()
start_message.speed(0)
start_message.color("white")
start_message.penup()
start_message.goto(0, 0)
start_message.write("Press Enter to Start", align="center",
                    font=("Courier", 48, "bold"))
pause_message.hideturtle()
pause_message.speed(0)
pause_message.color("white")
pause_message.penup()


def game_start():
    global started, bounces, start_message
    bounces = 0
    start_message.clear()
    started = True


def toggle_pause():
    global started, paused, pause_message
    if not started:
        return
    if not paused:
        pause_message.goto(0, 0)
        pause_message.write("Game Paused", align="center",
                            font=("Courier", 48, "bold"))
        pause_message.goto(0, -50)
        pause_message.write("Press 'P' to Unpause", align="center",
                            font=("Courier", 48, "bold"))
        paused = True
    else:
        pause_message.clear()
        paused = False


wn.onkeypress(game_start, "Return")
wn.onkeypress(toggle_pause, "p")
wn.onkeypress(toggle_pause, "P")
wn.onkeypress(wn.bye, "0")  # quit.


# Borders to bounce off - ball is a square of 20 with origin at center left
ball_height = ball_width = 20
window_right = wn.window_width() // 2
window_left = -window_right
window_top = (wn.window_height() - ball_height) // 2
window_bottom = -wn.window_height() // 2 + ball_height


# Main game loop.
while True:
    # Display.
    wn.update()
    if not started:
        continue
    elif paused:
        continue
    # Set speeds.
    if bounces == 0:
        reset_speeds()
        bounces += 1
    elif bounces % 10 == 0:
        accelerate_ball()
        accelerate_paddles()
        bounces += 1

    # Move the ball.
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border check - bounce ball off window top/bottom.  Play sound.
    if ball.ycor() > window_top:
        ball.sety(window_top)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    elif ball.ycor() < window_bottom:
        ball.sety(window_bottom)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    # Border check - continue ball from center after passing window
    # left/right. Reset bounce count and update scores.
    if ball.xcor() < window_left:
        ball.goto(0, 0)
        ball.dx *= -1
        bounces = 0
        os.system("afplay fail.mp3")
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a} Player B: {score_b}", align="center",
                  font=("Courier", 24, "normal"))
    elif ball.xcor() > window_right:
        ball.goto(0, 0)
        ball.dx *= - 1
        bounces = 0
        os.system("afplay fail.mp3")
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a} Player B: {score_b}", align="center",
                  font=("Courier", 24, "normal"))
    # Bounce ball off paddles. Update bounce count. Play sound.
    if -20 < ball.xcor() - paddle_b.xcor() < 10 and \
       -60 < ball.ycor() - paddle_b.ycor() < 60:
        ball.setx(paddle_b.xcor()-20)
        ball.dx *= -1
        bounces += 1
        print(f'Bounces: {bounces}')
        os.system("afplay bounce.wav&")
    elif -10 < ball.xcor() - paddle_a.xcor() < 20 and \
            -60 < ball.ycor() - paddle_a.ycor() < 60:
        ball.setx(paddle_a.xcor()+20)
        ball.dx *= -1
        bounces += 1
        print(f'Bounces: {bounces}')
        os.system("afplay bounce.wav&")
