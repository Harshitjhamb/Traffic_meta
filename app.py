import gradio as gr
import matplotlib.pyplot as plt
import imageio
from env import TrafficEnv
from models import Action

def run_simulation(steps=10):
    env = TrafficEnv()
    frames = []

    for _ in range(steps):
        env.step(Action(signal=0))

        plt.bar(range(4), env.lanes)
        plt.ylim(0, 20)
        plt.savefig("frame.png")
        plt.close()

        frames.append(imageio.imread("frame.png"))

    gif_path = "traffic.gif"
    imageio.mimsave(gif_path, frames, duration=0.5)

    return gif_path

demo = gr.Interface(
    fn=run_simulation,
    inputs=gr.Slider(1, 50, value=10, label="Steps"),
    outputs=gr.Image(type="filepath"),
    title="🚦 Traffic Simulation",
    description="Simulate traffic signal optimization"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)