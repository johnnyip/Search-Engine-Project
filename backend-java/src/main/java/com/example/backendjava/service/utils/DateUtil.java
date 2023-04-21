package com.example.backendjava.service.utils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DateUtil {
    
    private final static String date_format = "yyyy-MM-dd hh:mm:ss";
//    private final static String date_format = "yyyy-MM-dd";
    
    public static boolean isDateTwoAfterDateOne(String m_date_1, String m_date_2) {
        boolean isAfter = false;
        try {
            SimpleDateFormat format = new SimpleDateFormat(date_format);
            Date d1 = format.parse(m_date_1);
            Date d2 = format.parse(m_date_2);
            if(d1.compareTo(d2)<0) {
                isAfter = true;
            }
        } catch(ParseException e) {
            e.printStackTrace();
        }
        return isAfter;
    }
    
    public static String getFormattedDate(Date m_date) {
        String formatted_date = null;
        SimpleDateFormat format = new SimpleDateFormat(date_format);
        formatted_date = format.format(m_date);
        return formatted_date;
    }

    @SuppressWarnings("unused")
    public static void main(String[] args) {
        
//        try {
        
//            String date_format = "yyyy-mm-dd hh:mm:ss";
//            SimpleDateFormat format = new SimpleDateFormat(date_format);
//            Date d1 = format.parse("2023-04-19 08:18:20");
//            
//            System.out.println(d1);
//            System.out.println(getFormattedDate(d1));
//            
//            String str_d_1 = "2023-04-29 08:30:20";
//            String str_d_2 = "2023-04-20 12:12:12";
//            String str_d_3 = "2023-04-29 08:30:20";
//            System.out.println(isDateTwoAfterDateOne(str_d_2, str_d_3));
            
            Date d = new Date();
            System.out.println(getFormattedDate(d));
            
//        } catch(ParseException e) {
//            e.printStackTrace();
//        }

    }

}
