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

package test.jp.co.ns_sol.sysrdc.opal.gmtime;

import jp.co.ns_sol.sysrdc.opal.gmtime.GmtimeCalculator;
import jp.co.ns_sol.sysrdc.opal.gmtime.TmStruct;

/**
 * 単体テストクラス。
 * @author …
 */
public class MyGmtimeTest {

    /**
     * テスト用のメイン関数。
     * @param args
     */
    public static void main(String[] args) {
        TmStruct ts = null;
        ts = GmtimeCalculator.gmtime(946600000);
        System.out.print(ts.getYear());
        System.out.print("/");
        System.out.print(ts.getMon());
        System.out.print("/");
        System.out.print(ts.getMDay());
        System.out.print(" ");
        System.out.print(ts.getHour());
        System.out.print(".");
        System.out.print(ts.getMin());
        System.out.print(".");
        System.out.println(ts.getSec());

    }
};
