#include <stdio.h>
#include <string.h>

bool putInfo( char str[], char *substr1, char *substr2, FILE *output )
{
	char *p1, *p2;

	p1 = strstr(str, substr1);
	p2 = strstr(str, substr2);

	if(!p2 || !p2)
		return false;

	p1 += strlen(substr1);
	while(p1 < p2)
	{
		if(*p1 != ' ')
			fputc(*p1, output);
		p1++;
	}

	fputc(';', output);

	return true;
}

int main(int argc, const char *argv[])
{
	char str[500];
	FILE *input = fopen("conference_log_QP5.txt", "r");
	FILE *output = fopen("conference_stats.csv", "w");

	fprintf(output, "No;type;QP;size\n");

	while(fgets(str, 500, input))
	{
		if(putInfo(str, "frame=", "QP=", output) == false)
			continue;
		putInfo(str, "Slice:", "Poc:", output);
		putInfo(str, "QP=", "NAL=", output);
		putInfo(str, "size=", "bytes", output);
		fputc('\n', output);
	}

    return 0;
}
