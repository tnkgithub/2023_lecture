/*
 * ------------------------------------------------------------------------
 * 事業名：
 * 総務省
 *  最先端ネットワーク技術を活用した遠隔教育システムの開発・実証に係る請負
 * ------------------------------------------------------------------------
 * PLS（Programming　e-Learning　System）：
 * Java言語プログラミング演習
 * ------------------------------------------------------------------------
 */

package jp.co.ns_sol.sysrdc.opal.gmtime;

import java.time.Year;
import java.util.Calendar;
import java.util.TimeZone;


/**
 * …
 * @author …
 */
public class GmtimeCalculator {

    /**
     * 引数tに、1970年1月1日を起点とした Coordinated Universal Time (UTC)
     * の秒数を渡すと、
     * TmStruct のメンバに該当する日時の値をセットしてそれを返す。
     * @param t …
     * @return …
     */
    public static TmStruct gmtime(long t) {
        // カレンダーを取得
        Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
        // 秒数をミリ秒に変換してセット
        cal.setTimeInMillis(t * 1000L);
        // TmStructの各フィールドに対応する値をセット
        TmStruct tm = new TmStruct();
        tm.setSec(cal.get(Calendar.SECOND));
        tm.setMin(cal.get(Calendar.MINUTE));
        tm.setHour(cal.get(Calendar.HOUR_OF_DAY));
        tm.setMDay(cal.get(Calendar.DAY_OF_MONTH));
        tm.setMon(cal.get(Calendar.MONTH));
        tm.setYear(cal.get(Calendar.YEAR) - 1900);
        tm.setWDay(cal.get(Calendar.DAY_OF_WEEK) - 1);
        tm.setYDay(cal.get(Calendar.DAY_OF_YEAR) - 1);
        tm.setIsDst(cal.get(Calendar.DST_OFFSET) != 0 ? 1 : 0); // 夏時間かどうかの判定
        return tm;
    }

    // 必要なメンバがあれば適宜追加する。
};
