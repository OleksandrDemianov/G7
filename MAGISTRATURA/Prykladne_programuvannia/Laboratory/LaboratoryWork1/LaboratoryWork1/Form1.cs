using System.IO;

namespace LaboratoryWork1
{
    public partial class Form1 : Form
    {
        private bool valveTank1Open = false;
        private bool valveTank2Open = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void buttonValveTank1_Click(object sender, EventArgs e)
        {
            valveTank1Open = !valveTank1Open;

            string imagePath = valveTank1Open
                ? Path.Combine(AppContext.BaseDirectory, "Resources", "open.jpg")
                : Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank1.BackgroundImage = Image.FromFile(imagePath);

            if (valveTank1Open)
            {
                timerReleaseTank1.Stop();
                timerReleaseAll.Stop();
                timerTank1.Start();
            }
            else
            {
                timerTank1.Stop();

                string offAllImagePath =
                    Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

                pictureBox14.Image = Image.FromFile(offAllImagePath);
            }
        }

        private void timerTank1_Tick(object sender, EventArgs e)
        {
            if (progressBarTank1.Value < 100)
            {
                progressBarTank1.Value += 1;
                labelTank1Value.Text = progressBarTank1.Value + " %";
            }
            else
            {
                timerTank1.Stop();
            }
        }

        private void buttonValveTank2_Click(object sender, EventArgs e)
        {
            valveTank2Open = !valveTank2Open;

            string imagePath = valveTank2Open
                ? Path.Combine(AppContext.BaseDirectory, "Resources", "open.jpg")
                : Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank2.BackgroundImage = Image.FromFile(imagePath);

            if (valveTank2Open)
            {
                timerReleaseTank2.Stop();
                timerReleaseAll.Stop();
                timerTank2.Start();
            }
            else
            {
                timerTank2.Stop();

                string offAllImagePath =
                    Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

                pictureBox14.Image = Image.FromFile(offAllImagePath);
            }
        }

        private void timerTank2_Tick(object sender, EventArgs e)
        {
            if (progressBarTank2.Value < 100)
            {
                progressBarTank2.Value += 1;
                labelTank2Value.Text = progressBarTank2.Value + " %";
            }
            else
            {
                timerTank2.Stop();
            }
        }

        private void pictureBox15_Click(object sender, EventArgs e)
        {
            timerTank1.Stop();
            timerTank2.Stop();
            timerReleaseAll.Stop();
            timerReleaseTank1.Stop();
            timerReleaseTank2.Stop();

            progressBarTank1.Value = 0;
            progressBarTank2.Value = 0;

            labelTank1Value.Text = "0 %";
            labelTank2Value.Text = "0 %";

            valveTank1Open = false;
            valveTank2Open = false;

            string closedImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank1.BackgroundImage = Image.FromFile(closedImagePath);
            buttonValveTank2.BackgroundImage = Image.FromFile(closedImagePath);

            string offAllImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

            pictureBox14.Image = Image.FromFile(offAllImagePath);
        }

        private void pictureBox17_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void pictureBox14_Click(object sender, EventArgs e)
        {
            timerReleaseAll.Stop();
            timerReleaseTank1.Stop();
            timerReleaseTank2.Stop();

            valveTank1Open = true;
            valveTank2Open = true;

            string openImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "open.jpg");

            buttonValveTank1.BackgroundImage = Image.FromFile(openImagePath);
            buttonValveTank2.BackgroundImage = Image.FromFile(openImagePath);

            string onAllImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "onAll.png");

            pictureBox14.Image = Image.FromFile(onAllImagePath);

            timerTank1.Start();
            timerTank2.Start();
        }

        private void pictureBox16_Click(object sender, EventArgs e)
        {
            timerTank1.Stop();
            timerTank2.Stop();

            timerReleaseTank1.Stop();
            timerReleaseTank2.Stop();

            valveTank1Open = false;
            valveTank2Open = false;

            string closedImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank1.BackgroundImage = Image.FromFile(closedImagePath);
            buttonValveTank2.BackgroundImage = Image.FromFile(closedImagePath);

            string offAllImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

            pictureBox14.Image = Image.FromFile(offAllImagePath);

            timerReleaseAll.Start();
        }

        private void timerReleaseAll_Tick(object sender, EventArgs e)
        {
            if (progressBarTank1.Value > 0)
            {
                progressBarTank1.Value -= 1;
                labelTank1Value.Text = progressBarTank1.Value + " %";
            }

            if (progressBarTank2.Value > 0)
            {
                progressBarTank2.Value -= 1;
                labelTank2Value.Text = progressBarTank2.Value + " %";
            }

            if (progressBarTank1.Value == 0 &&
                progressBarTank2.Value == 0)
            {
                timerReleaseAll.Stop();
            }
        }

        private void pictureBox18_Click(object sender, EventArgs e)
        {
            timerTank1.Stop();
            timerReleaseAll.Stop();

            valveTank1Open = false;

            string closedImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank1.BackgroundImage = Image.FromFile(closedImagePath);

            string offAllImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

            pictureBox14.Image = Image.FromFile(offAllImagePath);

            timerReleaseTank1.Start();
        }

        private void timerReleaseTank1_Tick(object sender, EventArgs e)
        {
            if (progressBarTank1.Value > 0)
            {
                progressBarTank1.Value -= 1;
                labelTank1Value.Text = progressBarTank1.Value + " %";
            }

            if (progressBarTank1.Value == 0)
            {
                timerReleaseTank1.Stop();
            }
        }

        private void pictureBox19_Click(object sender, EventArgs e)
        {
            timerTank2.Stop();
            timerReleaseAll.Stop();

            valveTank2Open = false;

            string closedImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "closed.jpg");

            buttonValveTank2.BackgroundImage = Image.FromFile(closedImagePath);

            string offAllImagePath =
                Path.Combine(AppContext.BaseDirectory, "Resources", "offAll.png");

            pictureBox14.Image = Image.FromFile(offAllImagePath);

            timerReleaseTank2.Start();
        }

        private void timerReleaseTank2_Tick(object sender, EventArgs e)
        {
            if (progressBarTank2.Value > 0)
            {
                progressBarTank2.Value -= 1;
                labelTank2Value.Text = progressBarTank2.Value + " %";
            }

            if (progressBarTank2.Value == 0)
            {
                timerReleaseTank2.Stop();
            }
        }
    }
}
