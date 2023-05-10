using MahApps.Metro.Controls;
using MiniProject_AsosDaly.Logics;
using MiniProject_AsosDaly.Models;
using MySql.Data.MySqlClient;
using MySqlX.XDevAPI.Relational;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace MiniProject_AsosDaly
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

        // 조회
        private async void BtnReqRealtime_Click(object sender, RoutedEventArgs e)
        {

                string openApiUri = $"https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey=s86nUoT8OvF9KjCQEnAYi6kAQ56CU5iiqDHjh384K4gzAVzXj4qFqiCulxZJuhz9yfgwb87yUG%2FCmL1hD5RO%2Bg%3D%3D&pageNo=1&numOfRows=999&dataType=json&dataCd=ASOS&dateCd=DAY&startDt=20230101&endDt=20230509&stnIds=159";
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
                var status = Convert.ToInt32(jsonResult["response"]["header"]["resultCode"]);

                try
                {
                    if (status == 00) // 정상이면 데이터받아서 처리
                    {
                        var data = jsonResult["response"]["body"]["items"]["item"];
                        var json_array = data as JArray;

                        var asosdalys = new List<AsosDaly>();
                        foreach (var sensor in json_array)
                        {

                            asosdalys.Add(new AsosDaly
                            {
                                Idx = 0,
                                stnId = Convert.ToString(sensor["stnId"]),
                                stnNm = Convert.ToString(sensor["stnNm"]),
                                tm = Convert.ToString(sensor["tm"]),
                                avgTa = Convert.ToString(sensor["avgTa"]),
                                minTa = Convert.ToString(sensor["minTa"]),
                                minTaHrmt = Convert.ToString(sensor["minTaHrmt"]),
                                maxTa = Convert.ToString(sensor["maxTa"]),
                                maxTaHrmt = Convert.ToString(sensor["maxTaHrmt"]),
                                mi10MaxRn = Convert.ToString(sensor["mi10MaxRn"]),
                                mi10MaxRnHrmt = Convert.ToString(sensor["mi10MaxRnHrmt"]),
                                hr1MaxRn = Convert.ToString(sensor["hr1MaxRn"]),
                                hr1MaxRnHrmt = Convert.ToString(sensor["hr1MaxRnHrmt"]),
                                sumRnDur = Convert.ToString(sensor["sumRnDur"]),
                                sumRn = Convert.ToString(sensor["sumRn"]),
                                maxInsWs = Convert.ToString(sensor["maxInsWs"]),
                                maxInsWsWd = Convert.ToString(sensor["maxInsWsWd"]),
                                maxInsWsHrmt = Convert.ToString(sensor["maxInsWsHrmt"]),
                                maxWs = Convert.ToString(sensor["maxWs"]),
                                maxWsWd = Convert.ToString(sensor["maxWsWd"]),
                                maxWsHrmt = Convert.ToString(sensor["maxWsHrmt"]),
                                avgWs = Convert.ToString(sensor["avgWs"]),
                                hr24SumRws = Convert.ToString(sensor["hr24SumRws"]),
                                maxWd = Convert.ToString(sensor["maxWd"]),
                                avgTd = Convert.ToString(sensor["avgTd"]),
                                minRhm = Convert.ToString(sensor["minRhm"]),
                                minRhmHrmt = Convert.ToString(sensor["minRhmHrmt"]),
                                avgRhm = Convert.ToString(sensor["avgRhm"]),
                                avgPv = Convert.ToString(sensor["avgPv"]),
                                avgPa = Convert.ToString(sensor["avgPa"]),
                                maxPs = Convert.ToString(sensor["maxPs"]),
                                maxPsHrmt = Convert.ToString(sensor["maxPsHrmt"]),
                                minPs = Convert.ToString(sensor["minPs"]),
                                minPsHrmt = Convert.ToString(sensor["minPsHrmt"]),
                                avgPs = Convert.ToString(sensor["avgPs"]),
                                ssDur = Convert.ToString(sensor["ssDur"]),
                                sumSsHr = Convert.ToString(sensor["sumSsHr"]),
                                hr1MaxIcsrHrmt = Convert.ToString(sensor["hr1MaxIcsrHrmt"]),
                                hr1MaxIcsr = Convert.ToString(sensor["hr1MaxIcsr"]),
                                sumGsr = Convert.ToString(sensor["sumGsr"]),
                                ddMefs = Convert.ToString(sensor["ddMefs"]),
                                ddMefsHrmt = Convert.ToString(sensor["ddMefsHrmt"]),
                                ddMes = Convert.ToString(sensor["ddMes"]),
                                ddMesHrmt = Convert.ToString(sensor["ddMesHrmt"]),
                                sumDpthFhsc = Convert.ToString(sensor["sumDpthFhsc"]),
                                avgTca = Convert.ToString(sensor["avgTca"]),
                                avgLmac = Convert.ToString(sensor["avgLmac"]),
                                avgTs = Convert.ToString(sensor["avgTs"]),
                                minTg = Convert.ToString(sensor["minTg"]),
                                avgCm5Te = Convert.ToString(sensor["avgCm5Te"]),
                                avgCm10Te = Convert.ToString(sensor["avgCm10Te"]),
                                avgCm20Te = Convert.ToString(sensor["avgCm20Te"]),
                                avgCm30Te = Convert.ToString(sensor["avgCm30Te"]),
                                avgM05Te = Convert.ToString(sensor["avgM05Te"]),
                                avgM10Te = Convert.ToString(sensor["avgM10Te"]),
                                avgM15Te = Convert.ToString(sensor["avgM15Te"]),
                                avgM30Te = Convert.ToString(sensor["avgM30Te"]),
                                avgM50Te = Convert.ToString(sensor["avgM50Te"]),
                                sumLrgEv = Convert.ToString(sensor["sumLrgEv"]),
                                sumSmlEv = Convert.ToString(sensor["sumSmlEv"]),
                                n99Rn = Convert.ToString(sensor["n99Rn"]),
                                iscs = Convert.ToString(sensor["iscs"]),
                                sumFogDur = Convert.ToString(sensor["sumFogDur"])
                            });
                        }
                        this.DataContext = asosdalys;
                    }
                }
                catch (Exception ex)
                {
                    await Commons.ShowMessageAsync("오류", $"JSON 처리오류 {ex.Message}");
                }
            

            
        }

        // 저장
        private async void BtnSaveData_Click(object sender, RoutedEventArgs e)
        {
            if (GrdResult.Items.Count == 0)
            {
                await Commons.ShowMessageAsync("오류", "조회쫌하고 저장하세요.");
                return;
            }

            try
            {
                using (MySqlConnection conn = new MySqlConnection(Commons.ConnString))
                {
                    if (conn.State == System.Data.ConnectionState.Closed) conn.Open(); // db는 똑같음 외우기 
                    var query = @"INSERT INTO asosdaly
                                            (stnId,
                                            stnNm,
                                            tm,
                                            avgTa,
                                            minTa,
                                            minTaHrmt,
                                            maxTa,
                                            maxTaHrmt,
                                            mi10MaxRn,
                                            mi10MaxRnHrmt,
                                            hr1MaxRn,
                                            hr1MaxRnHrmt,
                                            sumRnDur,
                                            sumRn,
                                            maxInsWs,
                                            maxInsWsWd,
                                            maxInsWsHrmt,
                                            maxWs,
                                            maxWsWd,
                                            maxWsHrmt,
                                            avgWs,
                                            hr24SumRws,
                                            maxWd,
                                            avgTd,
                                            minRhm,
                                            minRhmHrmt,
                                            avgRhm,
                                            avgPv,
                                            avgPa,
                                            maxPs,
                                            maxPsHrmt,
                                            minPs,
                                            minPsHrmt,
                                            avgPs,
                                            ssDur,
                                            sumSsHr,
                                            hr1MaxIcsrHrmt,
                                            hr1MaxIcsr,
                                            sumGsr,
                                            ddMefs,
                                            ddMefsHrmt,
                                            ddMes,
                                            ddMesHrmt,
                                            sumDpthFhsc,
                                            avgTca,
                                            avgLmac,
                                            avgTs,
                                            minTg,
                                            avgCm5Te,
                                            avgCm10Te,
                                            avgCm20Te,
                                            avgCm30Te,
                                            avgM05Te,
                                            avgM10Te,
                                            avgM15Te,
                                            avgM30Te,
                                            avgM50Te,
                                            sumLrgEv,
                                            sumSmlEv,
                                            n99Rn,
                                            iscs,
                                            sumFogDur)
                                       VALUES
                                            (@stnId,
                                            @stnNm,
                                            @tm,
                                            @avgTa,
                                            @minTa,
                                            @minTaHrmt,
                                            @maxTa,
                                            @maxTaHrmt,
                                            @mi10MaxRn,
                                            @mi10MaxRnHrmt,
                                            @hr1MaxRn,
                                            @hr1MaxRnHrmt,
                                            @sumRnDur,
                                            @sumRn,
                                            @maxInsWs,
                                            @maxInsWsWd,
                                            @maxInsWsHrmt,
                                            @maxWs,
                                            @maxWsWd,
                                            @maxWsHrmt,
                                            @avgWs,
                                            @hr24SumRws,
                                            @maxWd,
                                            @avgTd,
                                            @minRhm,
                                            @minRhmHrmt,
                                            @avgRhm,
                                            @avgPv,
                                            @avgPa,
                                            @maxPs,
                                            @maxPsHrmt,
                                            @minPs,
                                            @minPsHrmt,
                                            @avgPs,
                                            @ssDur,
                                            @sumSsHr,
                                            @hr1MaxIcsrHrmt,
                                            @hr1MaxIcsr,
                                            @sumGsr,
                                            @ddMefs,
                                            @ddMefsHrmt,
                                            @ddMes,
                                            @ddMesHrmt,
                                            @sumDpthFhsc,
                                            @avgTca,
                                            @avgLmac,
                                            @avgTs,
                                            @minTg,
                                            @avgCm5Te,
                                            @avgCm10Te,
                                            @avgCm20Te,
                                            @avgCm30Te,
                                            @avgM05Te,
                                            @avgM10Te,
                                            @avgM15Te,
                                            @avgM30Te,
                                            @avgM50Te,
                                            @sumLrgEv,
                                            @sumSmlEv,
                                            @n99Rn,
                                            @iscs,
                                            @sumFogDur)";
                    var insRes = 0;
                    foreach (var temp in GrdResult.Items)
                    {
                        if (temp is AsosDaly)
                        {
                            var item = temp as AsosDaly;

                            MySqlCommand cmd = new MySqlCommand(query, conn);
                            cmd.Parameters.AddWithValue("@stnId", item.stnId);
                            cmd.Parameters.AddWithValue("@stnNm", item.stnNm);
                            cmd.Parameters.AddWithValue("@tm", item.tm);
                            cmd.Parameters.AddWithValue("@avgTa", item.avgTa);
                            cmd.Parameters.AddWithValue("@minTa", item.minTa);
                            cmd.Parameters.AddWithValue("@minTaHrmt", item.minTaHrmt);
                            cmd.Parameters.AddWithValue("@maxTa", item.maxTa);
                            cmd.Parameters.AddWithValue("@maxTaHrmt", item.maxTaHrmt);
                            cmd.Parameters.AddWithValue("@mi10MaxRn", item.mi10MaxRn);
                            cmd.Parameters.AddWithValue("@mi10MaxRnHrmt", item.mi10MaxRnHrmt);
                            cmd.Parameters.AddWithValue("@hr1MaxRn", item.hr1MaxRn);
                            cmd.Parameters.AddWithValue("@hr1MaxRnHrmt", item.hr1MaxRnHrmt);
                            cmd.Parameters.AddWithValue("@sumRnDur", item.sumRnDur);
                            cmd.Parameters.AddWithValue("@sumRn", item.sumRn);
                            cmd.Parameters.AddWithValue("@maxInsWs", item.maxInsWs);
                            cmd.Parameters.AddWithValue("@maxInsWsWd", item.maxInsWsWd);
                            cmd.Parameters.AddWithValue("@maxInsWsHrmt", item.maxInsWsHrmt);
                            cmd.Parameters.AddWithValue("@maxWs", item.maxWs);
                            cmd.Parameters.AddWithValue("@maxWsWd", item.maxWsWd);
                            cmd.Parameters.AddWithValue("@maxWsHrmt", item.maxWsHrmt);
                            cmd.Parameters.AddWithValue("@avgWs", item.avgWs);
                            cmd.Parameters.AddWithValue("@hr24SumRws", item.hr24SumRws);
                            cmd.Parameters.AddWithValue("@maxWd", item.maxWd);
                            cmd.Parameters.AddWithValue("@avgTd", item.avgTd);
                            cmd.Parameters.AddWithValue("@minRhm", item.minRhm);
                            cmd.Parameters.AddWithValue("@minRhmHrmt", item.minRhmHrmt);
                            cmd.Parameters.AddWithValue("@avgRhm", item.avgRhm);
                            cmd.Parameters.AddWithValue("@avgPv", item.avgPv);
                            cmd.Parameters.AddWithValue("@avgPa", item.avgPa);
                            cmd.Parameters.AddWithValue("@maxPs", item.maxPs);
                            cmd.Parameters.AddWithValue("@maxPsHrmt", item.maxPsHrmt);
                            cmd.Parameters.AddWithValue("@minPs", item.minPs);
                            cmd.Parameters.AddWithValue("@minPsHrmt", item.minPsHrmt);
                            cmd.Parameters.AddWithValue("@avgPs", item.avgPs);
                            cmd.Parameters.AddWithValue("@ssDur", item.ssDur);
                            cmd.Parameters.AddWithValue("@sumSsHr", item.sumSsHr);
                            cmd.Parameters.AddWithValue("@hr1MaxIcsrHrmt", item.hr1MaxIcsrHrmt);
                            cmd.Parameters.AddWithValue("@hr1MaxIcsr", item.hr1MaxIcsr);
                            cmd.Parameters.AddWithValue("@sumGsr", item.sumGsr);
                            cmd.Parameters.AddWithValue("@ddMefs", item.ddMefs);
                            cmd.Parameters.AddWithValue("@ddMefsHrmt", item.ddMefsHrmt);
                            cmd.Parameters.AddWithValue("@ddMes", item.ddMes);
                            cmd.Parameters.AddWithValue("@ddMesHrmt", item.ddMesHrmt);
                            cmd.Parameters.AddWithValue("@sumDpthFhsc", item.sumDpthFhsc);
                            cmd.Parameters.AddWithValue("@avgTca", item.avgTca);
                            cmd.Parameters.AddWithValue("@avgLmac", item.avgLmac);
                            cmd.Parameters.AddWithValue("@avgTs", item.avgTs);
                            cmd.Parameters.AddWithValue("@minTg", item.minTg);
                            cmd.Parameters.AddWithValue("@avgCm5Te", item.avgCm5Te);
                            cmd.Parameters.AddWithValue("@avgCm10Te", item.avgCm10Te);
                            cmd.Parameters.AddWithValue("@avgCm20Te", item.avgCm20Te);
                            cmd.Parameters.AddWithValue("@avgCm30Te", item.avgCm30Te);
                            cmd.Parameters.AddWithValue("@avgM05Te", item.avgM05Te);
                            cmd.Parameters.AddWithValue("@avgM10Te", item.avgM10Te);
                            cmd.Parameters.AddWithValue("@avgM15Te", item.avgM15Te);
                            cmd.Parameters.AddWithValue("@avgM30Te", item.avgM30Te);
                            cmd.Parameters.AddWithValue("@avgM50Te", item.avgM50Te);
                            cmd.Parameters.AddWithValue("@sumLrgEv", item.sumLrgEv);
                            cmd.Parameters.AddWithValue("@sumSmlEv", item.sumSmlEv);
                            cmd.Parameters.AddWithValue("@n99Rn", item.n99Rn);
                            cmd.Parameters.AddWithValue("@iscs", item.iscs);
                            cmd.Parameters.AddWithValue("@sumFogDur", item.sumFogDur);

                            insRes += cmd.ExecuteNonQuery();
                        }
                    }

                    await Commons.ShowMessageAsync("저장", "DB저장 성공!!!");
                }
            }
            catch (Exception ex)
            {
                await Commons.ShowMessageAsync("오류", $"DB저장 오류! {ex.Message}");
            }
        }

        
    }
}
