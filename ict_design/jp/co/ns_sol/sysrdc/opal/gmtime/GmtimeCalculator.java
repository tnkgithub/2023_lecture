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

import javax.swing.text.html.HTMLDocument.HTMLReader.IsindexAction;

/**
 * …
 *
 * @author …
 */
public class GmtimeCalculator {

    /**
     * 引数tに、1970年1月1日を起点とした Coordinated Universal Time (UTC)
     * の秒数を渡すと、
     * TmStruct のメンバに該当する日時の値をセットしてそれを返す。
     *
     * @param t …
     * @return …
     */
    public static TmStruct gmtime(long t) {
        // TmStructのインスタンスを生成する。
        TmStruct tm = new TmStruct();

        // 計算結果を格納する変数の初期値を設定
        int year = 1970;
        int month = 1;
        int day = 1;
        int hour = 0;
        int minute = 0;
        int second = 0;
        int dayOfWeek = 4; // 1970年1月1日は木曜日 (0:日曜日, 1:月曜日, ..., 6:土曜日)

        // 1日の秒数
        int secondsInDay = 24 * 60 * 60;

        // うるう年かどうかを判定
        boolean isLeapYear = false;
        if (year % 400 == 0) {
            isLeapYear = true;
        } else if (year % 100 == 0) {
            isLeapYear = false;
        } else if (year % 4 == 0) {
            isLeapYear = true;
        } else {
            isLeapYear = false;
        }

        // 年数を計算
        while (t >= secondsInDay * 365) {
            if (isLeapYear) {
                if (t >= secondsInDay * 366) {
                    t -= secondsInDay * 366;
                    year++;
                } else {
                    break;
                }
            } else {
                t -= secondsInDay * 365;
                year++;
            }
        }

        // 月数を計算
        int[] daysInMonth = { 31, isLeapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
        for (int i = 0; i < 12; i++) {
            if (t >= secondsInDay * daysInMonth[i]) {
                t -= secondsInDay * daysInMonth[i];
                month++;
            } else {
                break;
            }
        }
        // 日数を計算
        day = (int) (t / secondsInDay);
        t -= day * secondsInDay;

        // 時間数を計算
        hour = (int) (t / 3600);
        t -= hour * 3600;

        // 分数を計算
        minute = (int) (t / 60);
        t -= minute * 60;

        // 秒数を計算
        second = (int) t;

        // 曜日を計算
        dayOfWeek = (dayOfWeek + day) % 7;

        // TmStructのメンバに値をセット
        tm.setYear(year);
        tm.setMon(month);
        tm.setMDay(day);
        tm.setHour(hour);
        tm.setMin(minute);
        tm.setSec(second);
        tm.setWDay(dayOfWeek);

        return tm;
    }
}