using getFludMarksData.Logics;
using getFludMarksData.Models;
using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlTypes;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Xml;


namespace getFludMarksData.ViewModels
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        private static readonly string myKeyString = "BCJJ6H0U-BCJJ-BCJJ-BCJJ-BCJJ6H0UIV";
        private static readonly int pageNum = 1;
        private static readonly int numOfRows = 100;
        private static readonly string type = "XML"; // XML 밖에 지원을 안하는 듯함.

        private string insertQuery = $@"INSERT INTO miniproject01.getfludmarksdata
                                               (OBJT_ID,
                                               FLUD_SHIM,
                                               FLUD_GD,
                                               FLUD_AR,
                                               FLUD_YEAR,
                                               FLUD_NM,
                                               FLUD_NM2,
                                               SAT_DATE,
                                               END_DATE,
                                               SAT_TM,
                                               END_TM,
                                               CTPRVN_CD,
                                               SGG_CD,
                                               EMD_CD)
                                        VALUES
                                               (@OBJT_ID,
                                               @FLUD_SHIM,
                                               @FLUD_GD,
                                               @FLUD_AR,
                                               @FLUD_YEAR,
                                               @FLUD_NM,
                                               @FLUD_NM2,
                                               @SAT_DATE,
                                               @END_DATE,
                                               @SAT_TM,
                                               @END_TM,
                                               @CTPRVN_CD,
                                               @SGG_CD,
                                               @EMD_CD);";
        public MainWindow()
        {
            InitializeComponent();
        }

        public void InsertData(string query, List<string> add)
        {
            using (MySqlConnection conn = new MySqlConnection(Commons.myConnString))
            {
                if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                MySqlCommand cmd = new MySqlCommand(query, conn);
                foreach (char row in add[0])
                {
                    cmd.Parameters.AddWithValue("@OBJT_ID", add[0]);
                    cmd.Parameters.AddWithValue("@FLUD_SHIM", add[1]);
                    cmd.Parameters.AddWithValue("@FLUD_GD", add[2]);
                    cmd.Parameters.AddWithValue("@FLUD_AR", add[3]);
                    cmd.Parameters.AddWithValue("@FLUD_YEAR", add[4]);
                    cmd.Parameters.AddWithValue("@FLUD_NM", add[5]);
                    cmd.Parameters.AddWithValue("@FLUD_NM2", add[6]);
                    cmd.Parameters.AddWithValue("@SAT_DATE", add[7]);
                    cmd.Parameters.AddWithValue("@END_DATE", add[8]);
                    cmd.Parameters.AddWithValue("@SAT_TM", add[9]);
                    cmd.Parameters.AddWithValue("@END_TM", add[10]);
                    cmd.Parameters.AddWithValue("@CTPRVN_CD", add[11]);
                    cmd.Parameters.AddWithValue("@SGG_CD", add[12]);
                    cmd.Parameters.AddWithValue("@EMD_CD", add[13]);
                }
            }
        }
        // XML 파싱 & DB 저장
        private async void SetNaverXmlParseing(String strXml)
        {
            var adds = new List<List<string>>();

            XmlDocument xml = new XmlDocument(); // XmlDocument 생성
            xml.LoadXml(strXml);
            XmlNodeList fludMarksData = xml.GetElementsByTagName("item"); //접근할 노드

            if (fludMarksData != null)
            {
                foreach (XmlNode xn in fludMarksData)
                {
                    List<string> add = new List<string>();

                    add.Add(xn["OBJT_ID"].InnerText);
                    add.Add(xn["FLUD_SHIM"].InnerText);
                    add.Add(xn["FLUD_GD"].InnerText);
                    add.Add(xn["FLUD_AR"].InnerText);
                    add.Add(xn["FLUD_YEAR"].InnerText);
                    add.Add(xn["FLUD_NM"].InnerText);
                    add.Add(xn["FLUD_NM2"].InnerText);
                    add.Add(xn["SAT_DATE"].InnerText);
                    add.Add(xn["END_DATE"].InnerText);
                    add.Add(xn["SAT_TM"].InnerText);
                    add.Add(xn["END_TM"].InnerText);
                    add.Add(xn["CTPRVN_CD"].InnerText);
                    add.Add(xn["SGG_CD"].InnerText);
                    add.Add(xn["EMD_CD"].InnerText);

                    InsertData(insertQuery, add);
                }

            }
            else
            {
                this.DataContext = null;
                await Commons.ShowMessageAsync("오류", "API 오류");
            }
        }

        private async void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            string openApiUri = $@"http://safemap.go.kr/openApiService/data/getFludMarksData.do?serviceKey={myKeyString}&pageNo={pageNum}&numOfRows={numOfRows}&type={type}";
            string result = string.Empty;

            // WebRequest, WebResponse 객체
            WebRequest req = null;
            WebResponse res = null;
            StreamReader reader = null;

            try
            {
                req = WebRequest.Create(openApiUri);
                res = await req.GetResponseAsync();
                reader = new StreamReader(res.GetResponseStream());
                result = reader.ReadToEnd();

                Debug.WriteLine(result);
            }

            catch (Exception ex)
            {
                await Commons.ShowMessageAsync("오류", $"OpenAPI 조회오류 {ex.Message}");
            }

            try
            {
                SetNaverXmlParseing(result);
            }
            catch (Exception ex)
            {
                await Commons.ShowMessageAsync("오류", $"XML 처리오류 {ex.Message}");
            }
        }
    }
}
