using ControlzEx.Standard;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace getFludMarksData.Models
{
    public class getFludMarksDataApi
    {
        public int Idx { get; set; }
        public int OBJT_ID { get; set; }
        public double FLUD_SHIM { get; set; }
        public int FLUD_GD { get; set; }
        public double FLUD_AR { get; set; }
        public string FLUD_YEAR { get; set; }
        public string FLUD_NM { get; set; }
        public string FLUD_NM2 { get; set; }
        public string SAT_DATE { get; set; }
        public string END_DATE { get; set; }
        public string SAT_TM { get; set; }
        public string END_TM { get; set; }
        public string CTPRVN_CD { get; set; }
        public string SGG_CD { get; set; }
        public string EMD_CD { get; set; }

    }
}
