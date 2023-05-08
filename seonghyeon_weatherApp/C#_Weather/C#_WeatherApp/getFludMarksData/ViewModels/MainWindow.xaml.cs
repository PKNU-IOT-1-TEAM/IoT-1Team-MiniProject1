using getFludMarksData.Logics;
using getFludMarksData.Models;
using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Windows;
using System.Windows.Controls;

namespace getFludMarksData.ViewModels
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public static readonly string myKeyString = "BCJJ6H0U-BCJJ-BCJJ-BCJJ-BCJJ6H0UIV";
        public static readonly int pageNum = 1;
        public static readonly int numOfRows = 100;
        public static readonly string type = "JSON";

        public MainWindow()
        {
            InitializeComponent();
        }

        public void InsertData(string query, string dataname, DataGrid DtgResult)
        {
            using (MySqlConnection conn = new MySqlConnection(Commons.myConnString))
            {
                if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                MySqlCommand cmd = new MySqlCommand(query, conn);
                MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
                DataSet ds = new DataSet();
                adapter.Fill(ds);
                List<string> saveDateList = new List<string>();
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    saveDateList.Add(Convert.ToString(row[dataname]));
                }
                DtgResult.ItemsSource = saveDateList;
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

            var jsonResult = JObject.Parse(result);
            var resultCnt = Convert.ToInt32(jsonResult["response"]["body"]["items"]);

            try
            {
                if (resultCnt == 1) // 정상이면 데이터받아서 처리
                {
                    var data = jsonResult["item"];
                    var json_array = data as JArray;

                    var fludMarksData = new List<getFludMarksDataApi>();
                    foreach (var toilet in json_array)
                    {
                        fludMarksData.Add(new getFludMarksDataApi
                        {
                            idx = Convert.ToInt32(toilet["idx"]),
                            OBJT_ID = Convert.ToInt32(toilet["OBJT_ID"]),
                            FLUD_SHIM = Convert.ToInt32(toilet["FLUD_SHIM"]),
                            FLUD_GD = Convert.ToInt32(toilet["FLUD_GD"]),
                            FLUD_AR = Convert.ToInt32(toilet["FLUD_AR"]),
                            FLUD_YEAR = Convert.ToString(toilet["FLUD_YEAR"]),
                            FLUD_NM = Convert.ToString(toilet["FLUD_NM"]),
                            FLUD_NM2 = Convert.ToString(toilet["FLUD_NM2"]),
                            SAT_DATE = Convert.ToString(toilet["SAT_DATE"]),
                            END_DATE = Convert.ToString(toilet["END_DATE"]),
                            SAT_TM = Convert.ToString(toilet["SAT_TM"]),
                            END_TM = Convert.ToString(toilet["END_TM"]),
                            CTPRVN_CD = Convert.ToString(toilet["CTPRVN_CD"]),
                            SGG_CD = Convert.ToString(toilet["SGG_CD"]),
                            EMD_CD = Convert.ToString(toilet["EMD_CD"]),

                        });
                        this.DataContext = fludMarksData;
                    }
                }
                else
                {
                    this.DataContext = null;
                    await Commons.ShowMessageAsync("오류", "API 오류");
                }
            }
            catch (Exception ex)
            {
                await Commons.ShowMessageAsync("오류", $"JSON 처리오류 {ex.Message}");
            }
        }
    }
}
