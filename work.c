#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <dirent.h>
#include <sys/stat.h>

#ifdef _WIN32
#define ACCESS_CMD "if exist downloaded_images\\nul (exit 0) else (exit 1)"
#else
#define ACCESS_CMD "[ -d downloaded_images ]"
#endif

int count_image_files(const char *folder) {
    int count = 0;
    struct dirent *entry;
    DIR *dir = opendir(folder);

    if (!dir) return 0;

    while ((entry = readdir(dir)) != NULL) {
        if (strstr(entry->d_name, ".jpg") || strstr(entry->d_name, ".png")) {
            count++;
        }
    }

    closedir(dir);
    return count;
}

int main() {
    char url[1024];
    char command[2048];
    int image_count = 0;

    printf("🔗 Enter the full URL of the document page: ");
    fgets(url, sizeof(url), stdin);
    url[strcspn(url, "\n")] = 0;  // Remove trailing newline

    clock_t start_time = clock();


    snprintf(command, sizeof(command), "python ImgDownloader.py \"%s\"", url);
    printf("\n🚀 Starting image download process...\n");

    int download_status = system(command);
    if (download_status != 0) {
        printf("❌ ImgDownloader.py failed. Exiting.\n");
        return 1;
    }


    printf("\n🔎 Verifying downloaded images...\n");
    image_count = count_image_files("downloaded_images");

    if (image_count == 0) {
        printf("⚠️ No images found in 'downloaded_images/'. Cannot continue.\n");
        return 1;
    } else {
        printf("✅ Found %d image(s).\n", image_count);
    }


    printf("\n🧾 Converting downloaded images to PDF...\n");
    int pdf_status = system("python ImgToPdf.py");

    if (pdf_status != 0) {
        printf("❌ ImgToPdf.py failed. Exiting.\n");
        return 1;
    }

    clock_t end_time = clock();
    double total_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;


    printf("\n✅ Work Completed Successfully!\n");
    printf("🕒 Total time taken: %.2f seconds\n", total_time);
    return 0;
}
