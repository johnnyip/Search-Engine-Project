package com.example.backendjava.service.utils;

public class StringUtil {
    
    private static String special_characters = "\"`-=~!@#$%^&*()[]\\\\{}|;':\\\",./<>?\"";

    public static void main(String[] args) {
        String s = null;
        
        s = special_characters + "ABCabc123";
        replaceSpecialCharacterToSpace(s);
        
        
    }
    
    public static String replaceSpecialCharacterToSpace(String m_string) {
        String result = null;
        result = (m_string.replaceAll("[^0-9A-Za-z]", " ")).strip();
//        System.out.println("replaceSpecialCharacterToSpace.result: [" + result + "]");
        return result;
    }

}
