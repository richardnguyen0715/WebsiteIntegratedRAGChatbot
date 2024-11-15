# Git&Github Team Work Policy
**Author:** Richard Nguyen.
## Commit Policy:
### Syntax:
```bash
<name>_<action>_<files,folders>_<description (if needed)>
```
### Details:
1. Name: Tên của bạn.
2. Action: ADD (**ID: A**), UPDATE (**ID: U**), REMOVE (**ID: RM**), FIX (**ID: F**), RENAME (**ID: RN**), MERGE (**ID: M**), REVERT (**ID: RE**), PUSH (**ID: PS**), PULL (**ID: PL**), etc.
   * **ADD:** Thêm các tệp mới vào kho lưu trữ.
   * **UPDATE:** Cập nhật các tệp hiện có.
   * **REMOVE:** Xóa các tệp khỏi kho lưu trữ.
   * **RENAME:** Đổi tên các tệp.
   * **MERGE:** Kết hợp các nhánh.

        **Chú ý:** Với lệnh merge thì ghi với cú pháp **\<branch1>_\<branch2>**

   * **REVERT:** Hoàn tác các thay đổi từ một commit trước đó.

        ***Chú ý:** Phải ghi thêm thông tin là revert nhánh nào.*
   
   * **PUSH:** Đẩy các thay đổi lên Repo.

     ***Chú ý:** Phải ghi thêm thông tin là push nhánh nào.*
   
   * **PULL:** Kéo các thay đổi từ Repo về.
3. Notice:

    * Đối với các lệnh có tương tác ( **2 tham số trở lên** ) - ví dụ như MERGE,REVERT - thì cần commit luôn cả 2 tham số đó, cách nhau bởi **dấu gạch dưới.**

    * Khi công việc của bạn có nhiều phần thì ta sẽ **ghi theo ID** của các Action - mục 2. Các kí tự phân nhau bởi **dấu phẩy**.

4. Files | Folders: Là file thì ghi tiền tố Fi , là folder thì ghi tiền tố Fo. 

    **Ví dụ:** Fi-ReadMe.md , Fo-Requirements.

6. Description: Đây là phần mô tả ngắn gọn cho commit của mình. Viết ngắn thôi nhé! Nếu **không cần ghi** thì mình ghi **None**.

### Example:
1. **Tuong_ADD_Fi-README.md_Init-File-Readme:** Tường đã thêm một file readme.md vào trong repo.
2. **Tuong_A,U_Fi-README.md, Fo-Requirements_None:** Tường đã làm các hành động là thêm (**A**) và chỉnh sửa (**U**), nơi tác động là File README.md, Folder Requirements, Discription là None ( không có gì cả ). **(Không cần quan tâm đến action nào cho file nào ).**