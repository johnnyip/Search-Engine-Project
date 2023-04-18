package com.example.backendjava.service.utils;

public class Logger {
    
    public static void printHelloWorld() {
        System.out.println("Hello World!~");
    }
	
	public static void printStart(String m_proc_name) {
		System.out.println("\nStart [ " + m_proc_name + " ] ... ");
	}
	
	public static void printLevel1Info(String m_info) {
        System.out.print("--> " + m_info + " ... ");
    }
	
	public static void printLevelDone() {
        System.out.print("Done!" + "\n");
    }
	
	public static void printDone() {
		System.out.println("[ Done ]");
	}
	
	public static void printObject(Object o) {
        System.out.println("[" + o + "]");
    }
	
	public static void printKVPair(Object k, Object v) {
	    System.out.println("[" + k + "][" + v + "]");
	}

}
