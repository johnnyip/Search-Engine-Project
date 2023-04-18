package com.example.backendjava.service.utils;

import com.example.backendjava.service.IRUtilities.Porter;
import com.example.backendjava.service.core.Constants;

import java.io.*;
import java.util.HashSet;

public class StopStem
{
	private Porter porter;
	private HashSet<String> stopWords;
	public boolean isStopWord(String str)
	{
		return stopWords.contains(str);	
	}
	
//	public StopStem(String str)
	public StopStem()
	{
		super();
		porter = new Porter();
		stopWords = new HashSet<String>();
				
		// use BufferedReader to extract the stopwords in stopwords.txt (path passed as parameter str)
		// add them to HashSet<String> stopWords
		// MODIFY THE BELOW CODE AND ADD YOUR CODES HERE
//		stopWords.add("is");
//		stopWords.add("am");
//		stopWords.add("are");
//		stopWords.add("was");
//		stopWords.add("were");
		
		String line = null;
		try {
			BufferedReader reader = new BufferedReader(new FileReader(Constants.stopword_dict));
			while ((line = reader.readLine()) != null) {
//				System.out.println("[" + line + "]");
				stopWords.add(line);
			}
			reader.close();
			
		} catch(FileNotFoundException e) {
			e.printStackTrace();
		} catch(IOException e) {
			e.printStackTrace();
		}
		
	}
	public String stem(String str)
	{
		return porter.stripAffixes(str);
	}
	public static void main(String[] arg)
	{
//		StopStem stopStem = new StopStem("stopwords.txt");
		StopStem stopStem = new StopStem();
		String input="";
		try{
			do
			{
				System.out.print("Please enter a single English word: ");
				BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
				input = in.readLine();
				if(input.length()>0)
				{	
					if (stopStem.isStopWord(input))
						System.out.println("It should be stopped");
					else
			   			System.out.println("The stem of it is \"" + stopStem.stem(input)+"\"");
				}
			}
			while(input.length()>0);
		}
		catch(IOException ioe)
		{
			System.err.println(ioe.toString());
		}
	}
}
