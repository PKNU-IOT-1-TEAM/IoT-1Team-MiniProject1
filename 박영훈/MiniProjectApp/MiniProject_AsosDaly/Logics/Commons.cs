using MahApps.Metro.Controls.Dialogs;
using MahApps.Metro.Controls;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Net.Mime.MediaTypeNames;
using Application = System.Windows.Application;
    
namespace MiniProject_AsosDaly.Logics
{
    public class Commons
    {
        public static readonly string ConnString = "Server=210.119.12.66;" +
                                                     "Port=3306;" +
                                                     "Database=miniproject01;" +
                                                     "Uid=root;" +
                                                     "Pwd=12345;";

        public static async Task<MessageDialogResult> ShowMessageAsync(string title, string message,
            MessageDialogStyle style = MessageDialogStyle.Affirmative)
        {
            return await ((MetroWindow)Application.Current.MainWindow).ShowMessageAsync(title, message, style, null);
        }
    }
}
