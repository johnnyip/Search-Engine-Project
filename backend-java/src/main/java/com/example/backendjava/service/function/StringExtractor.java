package com.example.backendjava.service.function;

import com.example.backendjava.entity.PageContent;
import com.example.backendjava.entity.PageContentChildLink;
import org.htmlparser.Parser;
import org.htmlparser.beans.StringBean;
import org.htmlparser.filters.NodeClassFilter;
import org.htmlparser.tags.BodyTag;
import org.htmlparser.tags.LinkTag;
import org.htmlparser.tags.TitleTag;
import org.htmlparser.util.NodeList;
import org.htmlparser.util.ParserException;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class StringExtractor {

    //    private static String test_url = "https://cse.hkust.edu.hk/~dlee/4321/";
    public PageContent getPageContent(String baseUrl) {
//        ArrayList<String> pageContent = new ArrayList<>();
        PageContent pageContent = new PageContent();
        pageContent.setUrl(baseUrl);

        try {
            URL url = new URL(baseUrl);
            URLConnection connection = url.openConnection();
            long lastModified = connection.getLastModified();
            pageContent.setModifiedDate(new Date(lastModified));

            //
            StringBean stringBean = new StringBean();
            stringBean.setURL(baseUrl);
            Parser parser;
            NodeList list;

            //Page title
            parser = new Parser(baseUrl);
            list = parser.extractAllNodesThatMatch(new NodeClassFilter(TitleTag.class));
            for (int i = 0; i < list.size(); i++) {
                TitleTag title = (TitleTag) list.elementAt(i);
                pageContent.setTitle(title.getTitle());

            }

            //Child links
            parser = new Parser(baseUrl);
            list = parser.extractAllNodesThatMatch(new NodeClassFilter(LinkTag.class));
            List<PageContentChildLink> childLinks = new ArrayList<>();
            for (int i = 0; i < list.size(); i++) {
                LinkTag link = (LinkTag) list.elementAt(i);
                String link_ = link.getLink();
                if (link_.substring(0, 4).equals("http")) {
                    PageContentChildLink pageContentChildLink = new PageContentChildLink();
                    pageContentChildLink.setUrl(link_);
                    String linkText = link.getLinkText();
                    pageContentChildLink.setTitle(linkText);
                    childLinks.add(pageContentChildLink);
                }
            }
            pageContent.setChildList(childLinks);

            //Body
            String bodyText = "";
            parser = new Parser(baseUrl);
            list = parser.extractAllNodesThatMatch(new NodeClassFilter(BodyTag.class));
            for (int i = 0; i < list.size(); i++) {
                BodyTag tag = (BodyTag) list.elementAt(i);
                bodyText += tag.getBody().replaceAll("\\<.*?>", ""); // using a regular expression <.*?> to remove all HTML tags
            }
            pageContent.setWords(bodyText.split("\\s+"));


        } catch (ParserException e) {
            e.printStackTrace();
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return pageContent;
    }

}