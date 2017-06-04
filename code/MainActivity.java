package aaiijmrtt.awwnindya;

import android.app.*;
import android.os.*;
import android.view.*;
import android.view.View.*;
import android.widget.*;
import android.util.*;
import java.io.*;
import java.util.*;
import android.content.*;

public class MainActivity extends Activity {
	static String pattern = "^(\\d\\d)/(\\d\\d)/(\\d\\d\\d\\d), (\\d+):(\\d\\d) [AP]M - ([\\w ]*):(.*)$";
	static String initiator;
	static Vector<String> database;
	static int cursor;
	static TextView output;
	static EditText input;
	static Button send;
	static Context context;

	public static void parse(String filename) {
		try {
			BufferedReader br = new BufferedReader(new InputStreamReader(context.getAssets().open(filename)));
			String line = null, last = null, sofar = null;
			int index = -1;
			database = new Vector<String>();
			while((line = br.readLine()) != null)
				if(!line.matches(pattern))
					database.setElementAt(
						database.elementAt(index) +
						" " + line.trim(),
						index
					);
				else {
					if(last == null || !last.equals(line.replaceAll(pattern, "$6"))) {
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
					last = line.replaceAll(pattern, "$6");
				}
		}
		catch(Exception e) {
			Log.d("aaiijmrtt", "error reading database");
		}
	}

	public static String[] getWords(String string) {
		String result = new String();
		for(int i = 0; i < string.length(); ++i)
			if(Character.isLetter(string.charAt(i)) || Character.isSpaceChar(string.charAt(i)))
				result += Character.toLowerCase(string.charAt(i));
		return result.split("\\s+");
	}

	public static int getSimilarity(String string1, String string2) {
		if(string1.toLowerCase().equals(string2.toLowerCase()))
			return 1;
		return -1;
	}

	public static int smithwaterman(String lookup, String query) {
		String[] one = getWords(lookup), two = getWords(query);
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

	public static Vector<Integer> find(String query) {
		int maximum = -1, match;
		Vector<Integer> matches = new Vector<Integer>();
		for(int index = 0; index < database.size(); index++) {
			match = smithwaterman(database.elementAt(index), query);
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

	public static int next(String query, int cursor) {
		int best = -1;
		for(int proposal: find(query)) {
			best = proposal;
			if(proposal >= cursor)
				break;
		}
		return best + 1;
	}

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		context = getApplicationContext();
		parse("database.txt");
		cursor = -1;

		output = (TextView) findViewById(R.id.output);
		input = (EditText) findViewById(R.id.input);
		send = (Button) findViewById(R.id.send);
		OnClickListener sendClick = new OnClickListener() {
			public void onClick(View v) {
				String messagein = input.getText().toString(), messageout;
				cursor = next(messagein, cursor);
				if(cursor < database.size())
					messageout = database.elementAt(cursor);
				else
					messageout = database.elementAt(0);
				if(output.getLineCount() < 10)
					output.setText(output.getText().toString() + "\n >> " + messagein + "\n << " + messageout);
				else {
					String sofar = output.getText().toString();
					int index = sofar.indexOf("\n");
					sofar = sofar.substring(index + 1);
					index = sofar.indexOf("\n");
					output.setText(sofar.substring(index + 1) + "\n >> " + messagein + "\n << " + messageout);
				}
			}
		};
		send.setOnClickListener(sendClick);
	}
}
