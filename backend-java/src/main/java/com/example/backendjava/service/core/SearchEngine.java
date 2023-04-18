package com.example.backendjava.service.core;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import com.example.backendjava.service.utils.DBUtil;

public class SearchEngine extends Base {
    
    private static DBUtil db = null;
    private static Connection conn = null;
    private static ResultSet rs = null;
    
    private static ArrayList<Object> criteria;
    
    public static void main(String[] args) {
        
//        printKVPair("max_tf", getMaxTfByPageId(18, 2));
        
//      getFullUrlList();
      
      /*
       * [PageId][Url]
       * [296][https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm]
       */
//        getUrlByPageId(296);
//        getPageIdByUrl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm");
        
//        ArrayUtil.printArrayList(getAllUrlClearContent());
        
//        getStemIdByStem("apps");
    }
    
//    public static int getStemIdByStem(String m_stemTerm) {
//        int stemId = -1;
//        
//        try {
//            
//            db = new DBUtil();
//            conn = db.getConnection();
//            criteria = new ArrayList<Object>();
//            criteria.add(m_stemTerm);
//            rs = db.genericSearch(conn, ConstantsDB.selectStemIdByStemTerm, criteria);
//            if(rs.next()) {
//                stemId = rs.getInt("StemId");
//            }
//            conn.close();
//        } catch(SQLException e) {
//            e.printStackTrace();
//        }
//        System.out.println("[stemId][" + stemId + "]");
//        
//        return stemId;
//    }
    
    
    
    public static int getPageIdByUrl(String m_url) {
        int pageId = -1;
        
       try {
        
            db = new DBUtil();
            conn = db.getConnection();
            criteria = new ArrayList<Object>();
            criteria.add(m_url);
            rs = db.genericSearch(conn, ConstantsDB.selectPageIdByUrl, criteria);
            if(rs.next()) {
                pageId = rs.getInt("page_id");
            }
            
            conn.close();
       } catch(SQLException e) {
           e.printStackTrace();
       }
//       printKVPair(pageId, m_url);
       
       return pageId;
    }
    
//    public static String getUrlByPageId(int m_pageId) {
//        String url = "";
//        
//       try {
//        
//            db = new DBUtil();
//            conn = db.getConnection();
//            ArrayList<Object> criteria = new ArrayList<Object>();
//            criteria.add(m_pageId);
//            rs = db.genericSearch(conn, ConstantsDB.selectUrlByPageId, criteria);
//            if(rs.next()) {
//                url = rs.getString("Url");
//            }
//            
//            conn.close();
//       } catch(SQLException e) {
//           e.printStackTrace();
//       }
////       printKVPair(m_pageId, url);
//       
//       return url;
//        
//    }
    
    public static ArrayList<String> getFullUrlList(boolean m_with_page_id) {
        ArrayList<String> urlList = new ArrayList<String>();
        
        try {
            
            db = new DBUtil();
            conn = db.getConnection();
            rs = db.genericSearch(conn, ConstantsDB.selectAllUrl, null);
            
            while(rs.next()) {
                String pageId = rs.getString("page_id");
                String url = rs.getString("url");
                if(m_with_page_id) {
                    urlList.add(pageId+":"+url);
                } else {
                    urlList.add(url);
                }
            }
//            ArrayUtil.printArrayList(urlList);
            
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        return urlList;
    }
    
    public static ArrayList<String> getSrcWithPageId(String m_select_score) {
//        printKVPair("m_select_score", m_select_score);
        ArrayList<String> list = new ArrayList<String>();
        
        String query = "";
        
        if(m_select_score.equals(ConstantsDB.scopeAllRawTitle)) {
            query = ConstantsDB.selectAllRawTitleWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllRawContent)) {
            query = ConstantsDB.selectAllRawContentWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllClearTitle)) {
            query = ConstantsDB.selectAllClearTitleWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllClearContent)) {
            query = ConstantsDB.selectAllClearContentWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllStemTitle)) {
            query = ConstantsDB.selectAllStemTitleWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllStemContent)) {
            query = ConstantsDB.selectAllStemContentWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllClearTitleAndContent)) {
            query = ConstantsDB.selectAllClearTitleAndContentWithPageId;
        } else if(m_select_score.equals(ConstantsDB.scopeAllStemTitleAndContent)) {
            query = ConstantsDB.selectAllStemTitleAndContentWithPageId;
        } else {
            printHelloWorld();
        }
        
        try {
            db = new DBUtil();
            conn = db.getConnection();
            rs = db.genericSearch(conn, query, null);
            
            while(rs.next()) {
                String item = rs.getString("data");
                list.add(item);
            }
            
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        return list;
        
    }
    
    public static int getItemIdByItemName(String m_item_type, String m_item_name) {
        int itemId = -1;
        String query = null;
        
        if(m_item_type.equals(ConstantsDB.indexTypeTerm)) {
            query = ConstantsDB.selectTermIdByTerm;
        } else if(m_item_type.equals(ConstantsDB.indexTypeStem)) {
            query = ConstantsDB.selectStemIdByStem;
        }
        
        try {
            
            db = new DBUtil();
            conn = db.getConnection();
            criteria = new ArrayList<Object>();
            criteria.add(m_item_name);
            rs = db.genericSearch(conn, query, criteria);
            if(rs.next()) {
                itemId = rs.getInt("item_id");
            }
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
//        printKVPair(termId, m_term);
        
        return itemId;
    }
    
    public static ArrayList<Integer> getAllPageId() {
        ArrayList<Integer> list = new ArrayList<Integer>();
        
        try {
            db = new DBUtil();
            conn = db.getConnection();
            rs = db.genericSearch(conn, ConstantsDB.selectAllPageId, null);
            
            while(rs.next() ) {
                list.add(rs.getInt("page_id"));
            }
            
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        return list;
    }
    
    public static int getMaxTfByPageId(int m_pageId, int m_src_type) {
        int pageId = -1;
        
        try {
            db = new DBUtil();
            conn = db.getConnection();
            criteria = new ArrayList<Object>();
            criteria.add(m_pageId);
            criteria.add(m_src_type);
            
            rs = db.genericSearch(conn, ConstantsDB.selectMaxTfByPageId, criteria);
            
            if(rs.next()) {
                pageId = rs.getInt("max_tf");
            }
            
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        return pageId;
    }

}