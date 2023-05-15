using GalaSoft.MvvmLight;
using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using System;
using System.Data.SqlClient;
using System.Diagnostics;

namespace RiverLevelUI
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void MetroWindow_Loaded(object sender, System.Windows.RoutedEventArgs e)
        {
            MySqlConnection conn = new MySqlConnection("Server=pknuiot1team.cghin4qcf4s7.ap-northeast-2.rds.amazonaws.com;Port=3306;Database=miniproject02;Uid=pknuiot1team;Pwd=2V3lhihd8gIQ3krjNMf2;");

            conn.Open();

            // SELECT 문 실행
            MySqlCommand cmd = new MySqlCommand("SELECT * FROM ultrasrtfcst", conn);
            MySqlDataReader rdr = cmd.ExecuteReader();

            // 결과 출력
            while (rdr.Read())
            {
                string predict = "";
                string FcstDate = rdr["FcstDate"].ToString();
                string FcstTime = rdr["FcstTime"].ToString();

                string T1H = rdr["T1H"].ToString(); // 기온 (℃)
                string RN1 = rdr["RN1"].ToString(); // 1시간 강수량 (mm)
                string SKY = rdr["SKY"].ToString(); // 하늘상태
                string UUU = rdr["UUU"].ToString(); // 동서바람성분 (m/s)
                string VVV = rdr["VVV"].ToString(); // 남북바람성분 (m/s)
                string REH = rdr["REH"].ToString(); // 습도 (%)
                string PTY = rdr["PTY"].ToString(); // 강수형태 
                string LGT = rdr["LGT"].ToString(); // 낙뢰
                string VEC = rdr["VEC"].ToString(); // 풍향
                string WSD = rdr["WSD"].ToString(); // 풍속

                predict = $"{FcstDate.Substring(5,2)}월 {FcstDate.Substring(8, 2)}일 {FcstTime.Substring(0,2)}시 예보" +
                    $"\n기온은 {T1H}℃이며 습도는 {REH}%입니다. 풍향은 {VEC}deg, 풍속은 {WSD}m/s입니다." +
                    $"\n대기는 ";

                if (SKY == "1")
                {
                    predict += "맑을 것으로 예상됩니다. ";
                } else if (SKY == "3")
                {
                    predict += "구름이 많을 것으로 예상됩니다. ";
                } else if(SKY == "4")
                {
                    predict += "흐릴 것으로 예상됩니다. ";
                }

                if (PTY == "1" || PTY == "5")
                {
                    predict += $"{RN1}mm의 강수가 예상되며 ";
                }
                else if (PTY == "2" || PTY == "6")
                {
                    predict += "비 혹은 눈이 예상되며 ";
                }
                else if (PTY == "3" || PTY == "7")
                {
                    predict += "눈이 예상되며 ";
                }

                if (LGT != "0")
                {
                    predict += "낙뢰에 유의하기 바랍니다. ";
                }

                Txtpredict.Text = predict;

            }

            // 리소스 해제
            rdr.Close();
            conn.Close();
        }
    }
}
