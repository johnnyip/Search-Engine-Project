package com.example.backendjava.service.core;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Spider extends Base {
    
    private static Set<String> set = new LinkedHashSet<String>();
    
    public static ArrayList<String> getAllUrlList(String m_base_url) {
        ArrayList<String> list = new ArrayList<String>();
        fetchAllList(m_base_url);
        list.addAll(set);
        return list;
    }
    
    public static void fetchAllList(String m_url) {
        if(!set.contains(m_url) ) {
            try {
                set.add(m_url);
                Document doc = Jsoup.connect(m_url).get();
                Elements links = doc.select("a[href]");
                for(Element page: links) {
                    String link = page.attr("abs:href");
                    if(!set.contains(link)) {
                        fetchAllList(link);
                    }
                }
            } catch(IOException e) {
                e.printStackTrace();
            }
        }
        
    }
    
    public static ArrayList<String> getUrlChildLinks(String m_url) {
        ArrayList<String> list = new ArrayList<String>();
        Set<String> set = new LinkedHashSet<String>();
        
        try {
            
            Document doc = Jsoup.connect(m_url).get();
            Elements links = doc.select("a[href]");
            for(Element e : links) {
                String link = e.attr("abs:href"); 
//                printObject(link);
                set.add(link);
            }
            list.addAll(set);
            
        } catch(IOException e) {
            e.printStackTrace();
        }
//        ArrayUtil.printArrayList(list);
        
        return list;
    }
	
//	/**
//	 * (The stemmed item can be duplicated) 
//	 * 
//	 * @param m_content
//	 * @return
//	 */
//	public static ArrayList<String> getStopStemmedArrayList(String m_content) {
//		ArrayList<String> list = new ArrayList<String>();
//		
//		StopStem stopStem = new StopStem();
//		StringTokenizer st = new StringTokenizer(m_content, " ");
//        while(st.hasMoreTokens()) {
//        	String term = st.nextToken().strip();
//        	
//        	if(term.length()>0) {
//        		
//				if(stopStem.isStopWord(term)) {
//					// Ignore
////					System.out.println("==> [" + term + "] is a stop word!~");
//				} else {
////					String s = "before[" + term + "]";
//					term = stopStem.stem(term);
////					s += ", after[" + term + ']';
//					list.add(term);
////					System.out.println(s);
//				}
//			}
//        }
//        
//		return list;
//	}
	
	public static String normalizeString(String m_string) {
	    m_string = m_string.toLowerCase();
	    m_string = m_string.replaceAll("[^a-zA-Z0-9]", " "); 
        return m_string;
	}
	
//	public static UrlTO crawlPageContent(String m_url) {
////		System.out.println("Grap content from: [" + m_url + "]");
//		
//		UrlTO to = new UrlTO();
//		
//		String title = null;
//		String content = null;
//		String str_last_modified_date = null;
//		ArrayList<String> stop_stem_content = null;
//		
//		try {
//			
//			Document doc = Jsoup.connect(m_url).get();
//			title = doc.title();
//			content = doc.body().text();
////			content = content.toLowerCase();
////			content = content.replaceAll("[-/:.]", " ");
////			content = content.replaceAll("[?@,^|()\"'•©»&]", " ");
//			content = normalizeString(content);
//			
//			URL url = new URL("http://www.google.com");
//			url = new URL(m_url);
//		    HttpURLConnection httpCon = (HttpURLConnection) url.openConnection();
//		    str_last_modified_date = new Date(httpCon.getLastModified()).toString();
//		    stop_stem_content = getStopStemmedArrayList(content);
//		    
////		    System.out.println("title: [" + title + "]");
////		    System.out.println("content: [" + content + "]");
////		    System.out.println("str_last_modified_date: [" + str_last_modified_date + "]");
//		    
//		    to.setUrl(m_url);
//		    to.setTitle(title);
//		    to.setLast_modifed_date(str_last_modified_date);
//		    to.setRaw_content(content);
//		    to.setStop_stem_content(stop_stem_content);
//		
//		} catch(IOException e) {
//			e.printStackTrace();
//		}
//		
//		return to;
//	}

	public static void main(String[] args) {
//	    ArrayUtil.printArrayList(getAllUrlList(Constants.base_url));
//	    ArrayUtil.printArrayList(getUrlChildLinks("https://www.cse.ust.hk/~kwtleung/COMP4321/Movie.htm"));
	}

}
