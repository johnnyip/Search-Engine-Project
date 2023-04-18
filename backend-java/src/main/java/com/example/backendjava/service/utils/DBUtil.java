package com.example.backendjava.service.utils;

//import java.io.FileInputStream;
//import java.io.IOException;
//import java.io.InputStream;
//import java.util.Properties;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import com.example.backendjava.service.core.Base;
import com.example.backendjava.service.core.ConstantsDB;

import static com.example.backendjava.service.utils.Logger.printObject;

public class DBUtil extends Base {
    
//    private static Properties prop = null;
    private static Connection conn = null;
    
    public DBUtil() {
    
//        try {
//            InputStream is = new FileInputStream(Constants.properties_file);
//            prop = new Properties();
//            prop.load(is);
////            System.out.println(prop.getProperty("db.conn.url"));
//        } catch(IOException e) {
//            e.printStackTrace();
//        }
    }
    
    public ResultSet genericSearch(Connection m_conn, String m_query, ArrayList<Object> m_criteria) {
//        printKVPair(m_query, m_criteria);
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        
        try {
            pstmt = m_conn.prepareStatement(m_query);
            if(m_criteria!=null) {
                pstmt = this.fillPreparedStatement(pstmt, m_criteria);
            }
            
//            System.out.println(pstmt.toString());
            rs = pstmt.executeQuery();
        } catch(SQLException e) {
            System.err.println("Error m_conn: [" + m_conn + "]");
            System.err.println("Error m_query: [" + m_query + "]");
            System.err.println("Error pstmt: [" + pstmt + "]");
            System.err.println("Error m_criteria: [" + m_criteria + "]");
            System.err.println("Error rs: [" + rs + "]");
            e.printStackTrace();
        }
        
        return rs;
    }
    
    /*
     * Need to call commit() to update DB afterward,
     * as this method may be called by batch inserts
     */
    public void genericInsertUpdate(Connection m_conn, String m_insert_query, ArrayList<Object> m_data) {
//        System.out.println("insert data: " + m_data);
        PreparedStatement pstmt = null;
        
        try {
            pstmt = m_conn.prepareStatement(m_insert_query);
            if(m_data!=null) {
                pstmt = this.fillPreparedStatement(pstmt, m_data);
                int idx=1;
                for(Object data: m_data) {
                    pstmt.setObject(idx, data);
                    idx++;
                }
            }
//            System.out.println(pstmt);
//            printLevel1Info(pstmt.toString());
            pstmt.executeUpdate();
            
        } catch (SQLException e) {
            System.err.println("Error pstmt: [" + pstmt + "]");
            e.printStackTrace();
        }
    }
    
    private PreparedStatement fillPreparedStatement(PreparedStatement m_pstmt, ArrayList<Object> m_param) {
//        System.out.println("m_pstmt: [" + m_pstmt + "]");
//        System.out.println("m_param: " + m_param.toString());
        
        try {
            int idx=1;
            for(Object data: m_param) {
                m_pstmt.setObject(idx, data);
                idx++;
            }
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        return m_pstmt;
    }
    
    public Connection getConnection() {
        
        try {
            /*********************************
             * MySql
             *********************************/
//            conn_str = "jdbc:mysql://";
//            conn_str += prop.getProperty("db.conn.url");
//            conn_str += ":" + prop.getProperty("db.conn.port");
//            conn_str += "/" + prop.getProperty("db.conn.schema");
//            Class.forName("com.mysql.cj.jdbc.Driver");
//            conn = DriverManager.getConnection(conn_str, prop.getProperty("db.conn.usr"), prop.getProperty("db.conn.pwd"));
            
            /*********************************
             * SQLite
             *********************************/
            conn = DriverManager.getConnection("jdbc:sqlite:" + System. getProperty("user.dir") + ConstantsDB.dbFile);
            
            
            // for insertion interrup handling purpose. (i.e. ful transaction rollback)
            conn.setAutoCommit(false);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return conn;
    }

    public static void main(String[] args) {
        
        DBUtil db = new DBUtil();
        printObject(db.getConnection());
    }

}
