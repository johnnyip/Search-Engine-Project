package com.example.backendjava.service.utils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.StringTokenizer;

import com.example.backendjava.service.core.Base;

public class ArrayUtil extends Base {
    
    public static void printArrayList(ArrayList<?> m_obj) {
        for(Object o: m_obj) {
            printObject(o);
        }
    }
    
    public static void printSet(Set<?> m_set) {
        Iterator<?> itr = m_set.iterator();
        while (itr.hasNext()) {
            System.out.println(itr.next());
        }
    }
    
    public static ArrayList<String> getUniqueArrayList(ArrayList<String> m_list) {
        
        Set<String> set = new LinkedHashSet<String>();
        set.addAll(m_list);
        m_list.clear();
        m_list.addAll(set);
        
        return m_list;
    }
    
    @SuppressWarnings("unchecked")
    public static void countStringTermFrequency(Object m_list) {
        System.out.println(m_list.getClass());
        HashMap<String, Integer> map = new HashMap<String, Integer>();
        
        if(m_list instanceof ArrayList) {
            ArrayList<String> list = (ArrayList<String>)m_list;
            int init_count = 1;
            for(String key: list) {
//                System.out.println(key);
                int last_count = init_count;
                if(map.containsKey(key)) {
                    last_count = map.get(key)+1;
                }
                map.put(key, last_count);
            }
        } else if(m_list instanceof LinkedHashSet) {
            Set<String> keys = (Set<String>)m_list;
            int init_count = 1;
            for(String key: keys) {
//                System.out.println("key: [" + key + "]");
                int last_count = init_count;
                if(map.containsKey(key)) {
                    last_count = map.get(key)+1;
                }
                map.put(key, last_count);
            }
        }
        
//        System.out.println(map);
        Set<String> terms = map.keySet();
        for(String term: terms) {
            System.out.println(term + " [" + map.get(term) + "]");
        }
    }
    
    public static Set<String> getTermPositionMap(String m_content) {
        Set<String> tpSet = new LinkedHashSet<String>();
        
        StringTokenizer st = new StringTokenizer(m_content, " ");
        int pos = 1;
        while(st.hasMoreTokens()) {
            String term = st.nextToken().strip();
//            printKVPair(term, pos);
            String tp = term + "-" + pos;
            tpSet.add(tp);
            pos++;
        }
//        printSet(tpSet);
        
        return tpSet;
    }

    public static void main(String[] args) {
        
        String content = "this is the test page for a crawler before getting the admission of cse department of hkust  you should read through these international news and these books  here is my movie list  new";
        printSet(getTermPositionMap(content));
        
//        ArrayList<String> set = new ArrayList<String>();
//        set.add("aaa");
//        set.add("aaa");
//        set.add("aaa");
//        set.add("bbb");
//        set.add("bbb");
//        set.add("ccc");
//        set.add("ccc");
//        set.add("ccc");
//        set.add("ccc");
//        countStringTermFrequency(set);
        
//        ArrayList<String> list = new ArrayList<String>();
//        list.add("a"); list.add("a"); list.add("a"); list.add("a");
//        list.add("b"); list.add("b"); list.add("b");
//        list.add("c"); list.add("c");
//        System.out.println(list);
//        list = getUniqueArrayList(list);
//        System.out.println(list);
    }

}
