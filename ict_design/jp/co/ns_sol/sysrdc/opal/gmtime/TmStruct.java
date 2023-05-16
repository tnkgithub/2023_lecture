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

/**
 * 日付と時刻を年、月、日、時、分、秒のように分解して保持するクラス。
 * C言語のtime.hにあるtm構造体をJava言語で書き直したもの。
 * @author ...
 */
public final class TmStruct {

    /* 
     * 各フィールドの初期値にはデフォルト値を使用。
     * コンストラクタはデフォルトコンストラクタを使用。 
     */

    /** 
     * 秒 0-61(61まであるのは閏秒のため)
     */
    private int sec;

    /** 分 0-59 */
    private int min;

    /** 時 0-23 */
    private int hour;

    /** 日 1-31*/
    private int mDay;

    /** 月 0-11 */
    private int mon;

    /** 1900年からの年数 */
    private int year;

    /** 曜日 0:日 1:月 2:火 3:水 4:木 5:金 6:土 */
    private int wDay;

    /** 元日からの日数 0-365 */
    private int yDay;

    /** 
     * 夏時間フラグ<br>
     * 正数の場合は夏時間。
     * 0の場合は夏時間ではない。
     * 負数の場合は不明。
     */
    private int isDst;

    /**
     * 秒を取得する。
     * @return 秒 0-61(61まであるのは閏秒のため)
     */
    public int getSec() {
        return this.sec;
    }

    /**
     * 秒を設定する。
     * @param sec 秒 0-61(61まであるのは閏秒のため)
     */
    public void setSec(int sec) {
        this.sec = sec;
    }

    /**
     * 分を取得する。
     * @return 分 0-59
     */
    public int getMin() {
        return this.min;
    }

    /**
     * 分を設定する。
     * @param min 分 0-59
     */
    public void setMin(int min) {
        this.min = min;
    }

    /**
     * 時を取得する。
     * @return 時 0-23
     */
    public int getHour() {
        return this.hour;
    }

    /**
     * 時を設定する。
     * @param hour 時 0-23
     */
    public void setHour(int hour) {
        this.hour = hour;
    }

    /**
     * 日を取得する。
     * @return 日 1-31
     */
    public int getMDay() {
        return this.mDay;
    }

    /**
     * 日を設定する。
     * @param mDay 日 1-31
     */
    public void setMDay(int mDay) {
        this.mDay = mDay;
    }

    /**
     * 月を取得する。
     * @return 月 0-11
     */
    public int getMon() {
        return this.mon;
    }

    /**
     * 月を設定する。
     * @param mon 月 0-11
     */
    public void setMon(int mon) {
        this.mon = mon;
    }

    /**
     * 1900年からの年数を取得する。
     * @return 1900年からの年数
     */
    public int getYear() {
        return this.year;
    }

    /**
     * 1900年からの年数を設定する。
     * @param year 1900年からの年数
     */
    public void setYear(int year) {
        this.year = year;
    }

    /**
     * 曜日を取得する。
     * @return 曜日 0:日 1:月 2:火 3:水 4:木 5:金 6:土
     */
    public int getWDay() {
        return this.wDay;
    }

    /**
     * 曜日を設定する。
     * @param wDay 曜日 0:日 1:月 2:火 3:水 4:木 5:金 6:土
     */
    public void setWDay(int wDay) {
        this.wDay = wDay;
    }

    /**
     * 元日からの日数を取得する。
     * @return 元日からの日数 0-365
     */
    public int getYDay() {
        return this.yDay;
    }

    /**
     * 元日からの日数を設定する。
     * @param yDay 元日からの日数 0-365
     */
    public void setYDay(int yDay) {
        this.yDay = yDay;
    }

    /**
     * 夏時間フラグを取得する。
     * @return 夏時間フラグ。
     * 正数の場合は夏時間。
     * 0の場合は夏時間ではない。
     * 負数の場合は不明。
     */
    public int getIsDst() {
        return this.isDst;
    }

    /**
     * 夏時間フラグを設定する。
     * @param isDst 夏時間フラグ
     * 正数の場合は夏時間。
     * 0の場合は夏時間ではない。
     * 負数の場合は不明。
     */
    public void setIsDst(int isDst) {
        this.isDst = isDst;
    }
};
