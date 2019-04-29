using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;
using System.Windows.Forms;
using System.Threading;

namespace ComputerEyes
{
    class ComputerEyes
    {
        static void Main(string[] args)
        {
            int[, ,] rgb = new int[4,2,3];
            Console.WriteLine("Welcome to Screen Scanner");
            ScreenReader rd = new ScreenReader();
            
            Bitmap bmp = rd.screenshot();
            rgb = rd.readpixels(bmp);
            //Console.WriteLine("[{0}]", string.Join(", ", rgb));
            //Color color = bmp.GetPixel(50,50);
            //System.Threading.Thread.Sleep(5000);
        }
    }
    
    class ScreenReader
    {

        public Bitmap screenshot()
        {
            //Returns actual Screen as a Bitmap.
            System.Drawing.Size resolution = new System.Drawing.Size(1920,1080);
            
            var bmp = new Bitmap(1920,1080,PixelFormat.Format32bppArgb);
            // Create a graphics object from the bitmap.
            var gfxScreenshot = Graphics.FromImage(bmp);

            // Take the screenshot from the upper left corner to the right bottom corner.
            gfxScreenshot.CopyFromScreen(Screen.PrimaryScreen.Bounds.X, Screen.PrimaryScreen.Bounds.Y,0,0,resolution,CopyPixelOperation.SourceCopy);
            
            // Save the screenshot to the specified path that the user has chosen.
            //bmpScreenshot.Save("Screenshot.png", ImageFormat.Png);
            return bmp;
        }
        public int[, ,] readpixels(Bitmap bmp)
        {
            int[, ,] rgb = new int[4,1920, 1080];
            //Console.WriteLine("[{0}]", string.Join(", ", rgb));
            Color pixel = new Color();
            for (int i = 0; i < 1920; i++)
            {
                for (int j = 0; j < 1080; j++)
                {
                pixel = bmp.GetPixel(i,j);
                rgb[0,i,j] = pixel.A;
                rgb[1,i,j] = pixel.R;
                rgb[2,i,j] = pixel.G;
                rgb[3,i,j] = pixel.B;
                }
            }
            return rgb;
        }
    }
}
