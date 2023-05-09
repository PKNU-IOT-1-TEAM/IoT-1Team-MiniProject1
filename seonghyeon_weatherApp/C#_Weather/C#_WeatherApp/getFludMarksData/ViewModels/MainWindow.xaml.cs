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
using System.Linq;
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
        private static string myKeyString = "BCJJ6H0U-BCJJ-BCJJ-BCJJ-BCJJ6H0UIV";
        private static int pageNum = 1;
        private static int maxPageNum = 26;
        private static int maxNumOfRows = 25983;
        private static int numOfRows = 25983;
        private static string type = "XML"; // XML 밖에 지원을 안하는 듯함.

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

        public void InsertData(string query, List<getFludMarksDataApi> FludMarksData)
        {
            using (MySqlConnection conn = new MySqlConnection(Commons.myConnString))
            {
                if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                foreach (getFludMarksDataApi row in FludMarksData.ToArray())
                {
                    var item = row as getFludMarksDataApi;
                    MySqlCommand cmd = new MySqlCommand(query, conn);
                    cmd.Parameters.AddWithValue("@OBJT_ID", item.OBJT_ID);
                    cmd.Parameters.AddWithValue("@FLUD_SHIM", item.FLUD_SHIM);
                    cmd.Parameters.AddWithValue("@FLUD_GD", item.FLUD_GD);
                    cmd.Parameters.AddWithValue("@FLUD_AR", item.FLUD_AR);
                    cmd.Parameters.AddWithValue("@FLUD_YEAR", item.FLUD_YEAR);
                    cmd.Parameters.AddWithValue("@FLUD_NM", item.FLUD_NM);
                    cmd.Parameters.AddWithValue("@FLUD_NM2", item.FLUD_NM2);
                    cmd.Parameters.AddWithValue("@SAT_DATE", item.SAT_DATE);
                    cmd.Parameters.AddWithValue("@END_DATE", item.END_DATE);
                    cmd.Parameters.AddWithValue("@SAT_TM", item.SAT_TM);
                    cmd.Parameters.AddWithValue("@END_TM", item.END_TM);
                    cmd.Parameters.AddWithValue("@CTPRVN_CD", item.CTPRVN_CD);
                    cmd.Parameters.AddWithValue("@SGG_CD", item.SGG_CD);
                    cmd.Parameters.AddWithValue("@EMD_CD", item.EMD_CD);
                    
                    cmd.ExecuteNonQuery();
                }
            }
        }
        // XML 파싱 & DB 저장
        private async void FludMarksDataXmlParseing(String strXml)
        {
            XmlDocument xml = new XmlDocument(); // XmlDocument 생성
            xml.LoadXml(strXml);
            XmlNodeList FludMarksData = xml.GetElementsByTagName("item"); //접근할 노드

            if (FludMarksData != null)
            {
                var fludmarksdata = new List<getFludMarksDataApi>();

                foreach (XmlNode xn in FludMarksData)
                {
                    fludmarksdata.Add(new getFludMarksDataApi()
                    {
                        OBJT_ID = Convert.ToInt32(xn["OBJT_ID"].InnerText),
                        FLUD_SHIM = Convert.ToDouble(xn["FLUD_SHIM"].InnerText),
                        FLUD_GD = Convert.ToInt32(xn["FLUD_GD"].InnerText),
                        FLUD_AR = Convert.ToDouble(xn["FLUD_AR"].InnerText),
                        FLUD_YEAR = Convert.ToString(xn["FLUD_YEAR"].InnerText),
                        FLUD_NM = Convert.ToString(xn["FLUD_NM"].InnerText),
                        FLUD_NM2 = Convert.ToString(xn["FLUD_NM2"].InnerText),
                        SAT_DATE = Convert.ToString(xn["SAT_DATE"].InnerText),
                        END_DATE = Convert.ToString(xn["END_DATE"].InnerText),
                        SAT_TM = Convert.ToString(xn["SAT_TM"].InnerText),
                        END_TM = Convert.ToString(xn["END_TM"].InnerText),
                        CTPRVN_CD = Convert.ToString(xn["CTPRVN_CD"].InnerText),
                        SGG_CD = Convert.ToString(xn["SGG_CD"].InnerText),
                        EMD_CD = Convert.ToString(xn["EMD_CD"].InnerText),
                    });
                }
                InsertData(insertQuery, fludmarksdata);
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
                //for (int i = 1; i <= pageNum; i++) 
                //{ 
                //    if (pageNum > maxPageNum)
                //    {
                //        return;
                //    }
                //    else if (pageNum == 1)
                //    {
                FludMarksDataXmlParseing(result);
                //    }
                //}
            }
            catch (Exception ex)
            {
                await Commons.ShowMessageAsync("오류", $"XML 처리오류 {ex.Message}");
            }
        }
    }
}
