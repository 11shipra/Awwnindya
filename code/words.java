import java.io.*;
import java.util.*;

public class words {
	static String pattern = "^(\\d\\d)/(\\d\\d)/(\\d\\d\\d\\d), (\\d\\d):(\\d\\d) - ([\\w ]*):(.*)$";
	String initiator;
	Vector<String> database;

	public void parse(String filename) {
		try {
			BufferedReader br = new BufferedReader(new FileReader(filename));
			String line = null, last = null, sofar = null;
			int index = 0;
			database = new Vector<String>();
			while((line = br.readLine()) != null) {
				if(!line.matches(pattern))
					database.setElementAt(
						database.elementAt(index) +
						" " + line.trim(),
						index
					);
				else
					if(last == null || last.equals(line.replaceAll(pattern, "$6"))) {
						database.add(line.replaceAll(pattern, "$7").trim());
						index++;
						if(last == null)
							initiator = line.replaceAll(pattern, "$6");
					}
					else
						database.setElementAt(
							database.elementAt(index) +
							" " + line.replaceAll(pattern, "$7").trim(),
							index
						);
			}
		}
		catch(Exception e) {
			System.err.println(e.toString());
		}
	}

	public String[] getWords(String string) {
		String result = new String();
		for(int i = 0; i < string.length(); ++i)
			if(Character.isLetter(string.charAt(i)) || Character.isSpaceChar(string.charAt(i)))
				result += Character.toLowerCase(string.charAt(i));
		return result.split("\\s+");
	}

	public int getSimilarity(String string1, String string2) {
		if(string1.toLowerCase().equals(string2.toLowerCase()))
			return 1;
		return -1;
	}

	public int smithwaterman(String lookup, String query) {
		String[] one = getWords(lookup), two = getWords(lookup);
		int[][] table = new int [one.length + 1][two.length + 1];
		for(int i = 0; i < one.length; ++i)
			for(int ii = 0; ii < two.length; ++ii)
				table[i + 1][ii + 1] = Math.max(
					table[i][ii] + getSimilarity(one[i], two[ii]),
					Math.max(
						0,
						Math.max(
							table[i + 1][ii] - 1,
							table[i][ii + 1] - 1
						)
					)
				);
		int maximum = -1;
		for(int i = 0; i < one.length + 1; ++i)
			for(int ii = 0; ii < two.length + 1; ++ii)
				maximum = Math.max(maximum, table[i][ii]);
		return maximum;
	}

	public Vector<Integer> find(String query) {
		int maximum = -1, match;
		System.out.println(query);
		Vector<Integer> matches = new Vector<Integer>();
		for(int index = 0; index < database.size(); index++) {
			match = smithwaterman(database.elementAt(index), query);
			System.out.print(match + " ");
			if(maximum < match) {
				maximum = match;
				matches = new Vector<Integer>();
				matches.add(index);
			}
			else if(maximum == match)
				matches.add(index);
		}
		return matches;
	}

	public int next(String query, int cursor) {
		Vector<Integer> proposals = find(query);
		int best = -1;
		for(int proposal: proposals)
			if(proposal >= cursor) {
				best = proposal;
				break;
			}
		return best + 1;
	}
}
